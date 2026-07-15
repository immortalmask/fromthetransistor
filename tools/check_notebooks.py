#!/usr/bin/env python3
"""Validate and execute the course's cumulative, offline Jupyter notebooks."""

from __future__ import annotations

import argparse
import ast
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import traceback
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "course" / "notebooks.json"
CELL_ID = re.compile(r"^[A-Za-z0-9_-]+$")
NETWORK_MODULES = {"ftplib", "http", "requests", "smtplib", "socket", "ssl", "urllib"}


class NotebookError(RuntimeError):
    """A learner-facing notebook-suite error."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise NotebookError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise NotebookError(f"invalid JSON in {path}: {exc}") from exc


def safe_repo_path(relative: str, context: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise NotebookError(f"{context}: expected a non-empty relative path")
    candidate = (ROOT / relative).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise NotebookError(f"{context}: path escapes repository: {relative}") from exc
    return candidate


def safe_artifact_path(root: Path, relative: str, context: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise NotebookError(f"{context}: invalid artifact path")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise NotebookError(f"{context}: artifact path escapes its temporary root") from exc
    return candidate


def source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source")
    if isinstance(source, str):
        return source
    if isinstance(source, list) and all(isinstance(line, str) for line in source):
        return "".join(source)
    raise NotebookError("cell source must be a string or an array of strings")


def _import_roots(code: str, context: str) -> set[str]:
    tree = ast.parse(code, filename=context)
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


def validate_notebook(path: Path, module_ids: list[str]) -> tuple[dict[str, Any], int]:
    notebook = load_json(path)
    if not isinstance(notebook, dict) or notebook.get("nbformat") != 4:
        raise NotebookError(f"{path}: expected nbformat 4")
    if not isinstance(notebook.get("nbformat_minor"), int) or notebook["nbformat_minor"] < 5:
        raise NotebookError(f"{path}: expected nbformat_minor >= 5 with cell ids")
    if not isinstance(notebook.get("metadata"), dict):
        raise NotebookError(f"{path}: metadata must be an object")
    cells = notebook.get("cells")
    if not isinstance(cells, list) or len(cells) < 5:
        raise NotebookError(f"{path}: expected at least five cells")

    ids: set[str] = set()
    markdown_parts: list[str] = []
    code_parts: list[str] = []
    for index, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict) or cell.get("cell_type") not in {"markdown", "code"}:
            raise NotebookError(f"{path}: unsupported cell {index}")
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or not CELL_ID.fullmatch(cell_id) or cell_id in ids:
            raise NotebookError(f"{path}: invalid or duplicate cell id at {index}")
        ids.add(cell_id)
        if not isinstance(cell.get("metadata"), dict):
            raise NotebookError(f"{path}: cell {index} metadata must be an object")
        text = source_text(cell)
        if not text.strip():
            raise NotebookError(f"{path}: empty cell {index}")
        if cell["cell_type"] == "markdown":
            markdown_parts.append(text)
            continue
        if cell.get("execution_count") is not None or cell.get("outputs") != []:
            raise NotebookError(f"{path}: code cell {index} stores outputs or execution state")
        for line in text.splitlines():
            if line.lstrip().startswith(("%", "!")):
                raise NotebookError(f"{path}: code cell {index} uses a notebook magic or shell escape")
        compile(text, f"{path}#cell-{index}", "exec")
        code_parts.append(text)

    markdown = "\n".join(markdown_parts)
    code = "\n".join(code_parts)
    if "## Exercise" not in markdown:
        raise NotebookError(f"{path}: missing an Exercise section")
    if "Prerequisite" not in markdown:
        raise NotebookError(f"{path}: missing cumulative prerequisite text")
    missing_modules = [module_id for module_id in module_ids if module_id not in markdown]
    if missing_modules:
        raise NotebookError(f"{path}: prose does not map modules {missing_modules}")
    if "assert " not in code:
        raise NotebookError(f"{path}: missing executable self-checks")
    imports = _import_roots(code, str(path))
    third_party = imports - sys.stdlib_module_names
    if third_party:
        raise NotebookError(f"{path}: non-standard-library imports {sorted(third_party)}")
    network = imports & NETWORK_MODULES
    if network:
        raise NotebookError(f"{path}: network-capable imports are not allowed: {sorted(network)}")
    return notebook, len(code_parts)


def validate_manifest(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = load_json(path)
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise NotebookError("course/notebooks.json must be a schema-version 1 object")
    if not isinstance(document.get("course"), str) or not document["course"]:
        raise NotebookError("notebook manifest needs a course id")
    notebooks = document.get("notebooks")
    if not isinstance(notebooks, list) or not 4 <= len(notebooks) <= 5:
        raise NotebookError("notebook manifest must contain four or five ordered notebooks")

    catalog = load_json(ROOT / "course" / "catalog.json")
    known_modules = {
        module["id"]: safe_repo_path(module["path"], f"catalog module {module['id']}")
        for module in catalog.get("modules", [])
    }
    paths: set[str] = set()
    artifacts: set[str] = set()
    covered_modules: set[str] = set()
    ordered: list[dict[str, Any]] = []
    for index, entry in enumerate(notebooks, start=1):
        required = {"path", "title", "consumes", "emits", "modules"}
        if not isinstance(entry, dict) or set(entry) != required:
            raise NotebookError(f"notebook {index}: expected fields {sorted(required)}")
        path_value = entry["path"]
        notebook_path = safe_repo_path(path_value, f"notebook {index}")
        if notebook_path.suffix != ".ipynb" or not notebook_path.is_file():
            raise NotebookError(f"notebook {index}: missing .ipynb file {path_value}")
        if path_value in paths:
            raise NotebookError(f"duplicate notebook path: {path_value}")
        paths.add(path_value)
        if not isinstance(entry["title"], str) or not entry["title"].strip():
            raise NotebookError(f"notebook {index}: title must be non-empty")
        modules = entry["modules"]
        if (
            not isinstance(modules, list)
            or not modules
            or any(not isinstance(item, str) for item in modules)
            or len(modules) != len(set(modules))
        ):
            raise NotebookError(f"notebook {index}: modules must be a unique string array")
        unknown = set(modules) - set(known_modules)
        if unknown:
            raise NotebookError(f"notebook {index}: unknown modules {sorted(unknown)}")
        missing_pages = [item for item in modules if not known_modules[item].is_file()]
        if missing_pages:
            raise NotebookError(f"notebook {index}: missing module pages {missing_pages}")
        overlap = covered_modules & set(modules)
        if overlap:
            raise NotebookError(f"notebook {index}: duplicate module mappings {sorted(overlap)}")
        covered_modules.update(modules)
        consumes = entry["consumes"]
        if not isinstance(consumes, list) or any(not isinstance(item, str) for item in consumes):
            raise NotebookError(f"notebook {index}: consumes must be a string array")
        unavailable = set(consumes) - artifacts
        if unavailable:
            raise NotebookError(f"notebook {index}: unavailable artifacts {sorted(unavailable)}")
        for consumed in consumes:
            safe_artifact_path(Path("/tmp/artifacts"), consumed, f"notebook {index}")
        emitted = entry["emits"]
        safe_artifact_path(Path("/tmp/artifacts"), emitted, f"notebook {index}")
        if emitted in artifacts:
            raise NotebookError(f"notebook {index}: duplicate emitted artifact {emitted}")
        if index > 1 and not consumes:
            raise NotebookError(f"notebook {index}: later notebooks must consume prior evidence")
        artifacts.add(emitted)
        validate_notebook(notebook_path, modules)
        ordered.append(entry)
    return document, ordered


def execute_notebook(path: Path, module_ids: list[str], artifact_root: Path, show_stdout: bool) -> int:
    notebook, code_count = validate_notebook(path, module_ids)
    namespace: dict[str, Any] = {"__name__": "__main__", "__builtins__": __builtins__}
    output = io.StringIO()
    previous = os.environ.get("COURSE_NOTEBOOK_ARTIFACTS")
    os.environ["COURSE_NOTEBOOK_ARTIFACTS"] = str(artifact_root)
    try:
        for index, cell in enumerate(notebook["cells"], start=1):
            if cell["cell_type"] != "code":
                continue
            with redirect_stdout(output):
                exec(
                    compile(source_text(cell), f"{path}#cell-{index}", "exec"),
                    namespace,
                )
    finally:
        if previous is None:
            os.environ.pop("COURSE_NOTEBOOK_ARTIFACTS", None)
        else:
            os.environ["COURSE_NOTEBOOK_ARTIFACTS"] = previous
    if show_stdout and output.getvalue():
        print(output.getvalue(), end="")
    return code_count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--show-stdout", action="store_true")
    args = parser.parse_args(argv)
    try:
        _, ordered = validate_manifest(args.manifest.resolve())
        if args.validate_only:
            for entry in ordered:
                _, count = validate_notebook(
                    safe_repo_path(entry["path"], "notebook"), entry["modules"]
                )
                print(f"VALID {entry['path']} ({count} code cells)")
            print(f"PASS: {len(ordered)} notebooks validated; no stored outputs")
            return 0
        with tempfile.TemporaryDirectory(prefix="course-notebook-artifacts-") as temporary:
            artifact_root = Path(temporary)
            for entry in ordered:
                for consumed in entry["consumes"]:
                    if not safe_artifact_path(artifact_root, consumed, "consumed artifact").is_file():
                        raise NotebookError(f"{entry['path']}: missing consumed artifact {consumed}")
                count = execute_notebook(
                    safe_repo_path(entry["path"], "notebook"),
                    entry["modules"],
                    artifact_root,
                    args.show_stdout,
                )
                emitted = safe_artifact_path(artifact_root, entry["emits"], "emitted artifact")
                if not emitted.is_file():
                    raise NotebookError(f"{entry['path']}: did not emit {entry['emits']}")
                load_json(emitted)
                print(f"PASS  {entry['path']} ({count} code cells; {entry['emits']})")
        print(f"PASS: {len(ordered)} notebooks executed cumulatively in a temporary artifact root")
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        if not isinstance(exc, NotebookError):
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

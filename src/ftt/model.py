"""Catalog and Markdown loading for the course runner."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from typing import Any


class CourseError(RuntimeError):
    """A learner-facing course configuration or usage error."""


ID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{1,63}$")


def find_root(explicit: str | Path | None = None) -> Path:
    """Find the repository root without depending on the current directory."""

    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    if os.environ.get("FTT_ROOT"):
        candidates.append(Path(os.environ["FTT_ROOT"]))
    candidates.extend([Path.cwd(), Path(__file__).resolve().parents[2]])

    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        for parent in (candidate, *candidate.parents):
            if (parent / "course" / "catalog.json").is_file():
                return parent
    raise CourseError(
        "Could not find course/catalog.json. Run from the repository or pass --root."
    )


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    """Parse the deliberately small YAML subset used by vault pages.

    Scalar values, JSON-style arrays, quoted strings, booleans, and numbers are
    supported. Keeping the subset small makes the checkout dependency-free.
    """

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    data: dict[str, Any] = {}
    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise CourseError(f"Invalid frontmatter line in {path}: {line!r}")
        key, raw = line.split(":", 1)
        key, raw = key.strip(), raw.strip()
        if not key:
            raise CourseError(f"Empty frontmatter key in {path}")
        if key in data:
            raise CourseError(f"Duplicate frontmatter key {key!r} in {path}")
        if raw == "":
            data[key] = ""
            continue
        try:
            data[key] = json.loads(raw)
        except json.JSONDecodeError:
            lowered = raw.lower()
            if lowered in {"true", "false"}:
                data[key] = lowered == "true"
            else:
                data[key] = raw
    if end is None:
        raise CourseError(f"Unclosed frontmatter in {path}")
    body = "\n".join(lines[end + 1 :])
    if text.endswith("\n"):
        body += "\n"
    return data, body


@dataclass(frozen=True)
class Catalog:
    root: Path
    raw: dict[str, Any]

    @classmethod
    def load(cls, root: Path) -> "Catalog":
        path = root / "course" / "catalog.json"
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise CourseError(f"Missing catalog: {path}") from exc
        except json.JSONDecodeError as exc:
            raise CourseError(f"Invalid JSON in {path}: {exc}") from exc
        if raw.get("schema_version") != 1:
            raise CourseError("Unsupported catalog schema_version (expected 1)")
        return cls(root=root, raw=raw)

    @property
    def course(self) -> dict[str, Any]:
        return self.raw["course"]

    @property
    def sections(self) -> list[dict[str, Any]]:
        return self.raw["sections"]

    @property
    def modules(self) -> list[dict[str, Any]]:
        return self.raw["modules"]

    @property
    def exams(self) -> list[dict[str, Any]]:
        return self.raw.get("exams", [])

    @property
    def toolchain(self) -> list[dict[str, Any]]:
        return self.raw.get("toolchain", [])

    def module(self, module_id: str) -> dict[str, Any]:
        for module in self.modules:
            if module["id"] == module_id or module.get("slug") == module_id:
                return module
        raise CourseError(f"Unknown module: {module_id}")

    def section(self, section_id: str) -> dict[str, Any]:
        for section in self.sections:
            if section["id"] == section_id or section.get("slug") == section_id:
                return section
        raise CourseError(f"Unknown section: {section_id}")

    def exam(self, exam_id: str) -> dict[str, Any]:
        for exam in self.exams:
            if exam["id"] == exam_id:
                return exam
        raise CourseError(f"Unknown exam: {exam_id}")

    def lab_id(self, target: str) -> str:
        if not ID_PATTERN.fullmatch(target):
            raise CourseError(f"Invalid module/lab id: {target!r}")
        lab_dir = self.safe_path(Path("labs") / target)
        if (lab_dir / "lab.json").is_file():
            return target
        module = self.module(target)
        if not module.get("lab"):
            raise CourseError(f"Module {module['id']} has no automated lab")
        return str(module["lab"])

    def lab_spec(self, lab_id: str) -> dict[str, Any]:
        if not ID_PATTERN.fullmatch(lab_id):
            raise CourseError(f"Invalid lab id: {lab_id!r}")
        path = self.safe_path(Path("labs") / lab_id / "lab.json")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise CourseError(f"Missing lab specification: {path}") from exc
        except json.JSONDecodeError as exc:
            raise CourseError(f"Invalid lab specification {path}: {exc}") from exc

    def page_path(self, item: dict[str, Any]) -> Path:
        return self.safe_path(item["path"])

    def safe_path(self, relative: str | Path) -> Path:
        candidate = Path(relative)
        if candidate.is_absolute():
            raise CourseError(f"Course path must be relative: {relative}")
        resolved = (self.root / candidate).resolve()
        try:
            resolved.relative_to(self.root.resolve())
        except ValueError as exc:
            raise CourseError(f"Course path escapes repository: {relative}") from exc
        return resolved

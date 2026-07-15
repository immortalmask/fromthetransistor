"""Structural validation for catalog, vault, labs, and exams."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
from typing import Any

from .challenges import ChallengeCatalog, validate_challenges
from .model import Catalog, CourseError, parse_frontmatter
from .runner import validate_lab_spec


REQUIRED_HEADINGS = (
    "## Why this block exists",
    "## Lecture",
    "## Workbook",
    "## Problem set",
    "## Homework",
    "## Reverse-engineering lens",
    "## External sources",
    "## Exit criteria",
)

REFERENCE_KINDS = {"course", "manual", "specification", "project", "paper", "datasheet"}
REFERENCE_TIERS = {"start", "reference", "deeper"}
REFERENCE_START = "<!-- ftt:references:start -->"
REFERENCE_END = "<!-- ftt:references:end -->"


def _duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def _check_graph(modules: list[dict[str, Any]], errors: list[str]) -> None:
    by_id = {module["id"]: module for module in modules}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(module_id: str) -> None:
        if module_id in visiting:
            errors.append(f"prerequisite cycle reaches {module_id}")
            return
        if module_id in visited:
            return
        visiting.add(module_id)
        for requirement in by_id[module_id].get("prerequisites", []):
            if requirement not in by_id:
                errors.append(f"{module_id}: unknown prerequisite {requirement}")
            else:
                visit(requirement)
        visiting.remove(module_id)
        visited.add(module_id)

    for module_id in by_id:
        visit(module_id)


def validate(catalog: Catalog) -> list[str]:
    errors: list[str] = []
    modules = catalog.modules
    sections = catalog.sections
    module_ids = [module.get("id", "") for module in modules]
    section_ids = [section.get("id", "") for section in sections]
    for duplicate in sorted(_duplicates(module_ids)):
        errors.append(f"duplicate module id: {duplicate}")
    for duplicate in sorted(_duplicates(section_ids)):
        errors.append(f"duplicate section id: {duplicate}")
    _check_graph(modules, errors)

    known_sections = set(section_ids)
    source_refs: list[str] = []
    labs_seen: set[str] = set()
    for module in modules:
        module_id = module.get("id", "<missing>")
        if module.get("section") not in known_sections:
            errors.append(f"{module_id}: unknown section {module.get('section')}")
        try:
            path = catalog.safe_path(module.get("path", ""))
        except CourseError as exc:
            errors.append(f"{module_id}: {exc}")
            continue
        if not path.is_file():
            errors.append(f"{module_id}: missing page {path.relative_to(catalog.root)}")
        else:
            try:
                metadata, body = parse_frontmatter(path)
                if metadata.get("id") != module_id:
                    errors.append(f"{module_id}: frontmatter id mismatch in {path}")
                if metadata.get("title") != module.get("title"):
                    errors.append(f"{module_id}: frontmatter title mismatch in {path}")
                if str(metadata.get("section")) != str(module.get("section")):
                    errors.append(f"{module_id}: frontmatter section mismatch in {path}")
                for heading in REQUIRED_HEADINGS:
                    if heading not in body:
                        errors.append(f"{module_id}: missing heading {heading!r}")
            except CourseError as exc:
                errors.append(str(exc))
        if module.get("source_ref"):
            source_refs.append(module["source_ref"])
        if module.get("lab"):
            lab_id = module["lab"]
            labs_seen.add(lab_id)
            try:
                spec_path = catalog.safe_path(Path("labs") / lab_id / "lab.json")
            except CourseError as exc:
                errors.append(f"{module_id}: {exc}")
                continue
            for expected in (
                spec_path,
                spec_path.parent / "starter",
                spec_path.parent / "solution",
                spec_path.parent / "Makefile",
                spec_path.parent / "tests" / "test.c",
            ):
                if not expected.exists():
                    errors.append(f"{module_id}: missing lab asset {expected.relative_to(catalog.root)}")
            if spec_path.is_file():
                try:
                    spec = json.loads(spec_path.read_text(encoding="utf-8"))
                    spec = validate_lab_spec(spec, expected_id=lab_id)
                    if spec.get("module") != module_id:
                        errors.append(f"{module_id}: lab module mismatch for {lab_id}")
                except (CourseError, json.JSONDecodeError) as exc:
                    errors.append(f"{lab_id}: invalid JSON: {exc}")

    for shared_native_asset in (
        catalog.root / "labs" / "c-test.mk",
        catalog.root / "labs" / "test_support.h",
        catalog.root / "tools" / "sync_native_c_tests.py",
    ):
        if not shared_native_asset.is_file():
            errors.append(
                f"missing native C test asset "
                f"{shared_native_asset.relative_to(catalog.root)}"
            )

    outline_path = catalog.root / "course" / "source-outline.json"
    if outline_path.is_file():
        outline = json.loads(outline_path.read_text(encoding="utf-8"))
        expected_refs = [item["id"] for item in outline["items"]]
        if set(source_refs) != set(expected_refs):
            errors.append(
                "source coverage mismatch: "
                f"missing={sorted(set(expected_refs) - set(source_refs))}, "
                f"extra={sorted(set(source_refs) - set(expected_refs))}"
            )
        for duplicate in sorted(_duplicates(source_refs)):
            errors.append(f"source outline item mapped more than once: {duplicate}")
    else:
        errors.append("missing course/source-outline.json")

    exam_ids = [exam.get("id", "") for exam in catalog.exams]
    for duplicate in sorted(_duplicates(exam_ids)):
        errors.append(f"duplicate exam id: {duplicate}")
    for exam in catalog.exams:
        for key in ("path", "bank"):
            try:
                path = catalog.safe_path(exam.get(key, ""))
            except CourseError as exc:
                errors.append(f"{exam.get('id')}: {exc}")
                continue
            if not path.is_file():
                errors.append(f"{exam.get('id')}: missing {key} {path.relative_to(catalog.root)}")
        try:
            bank_path = catalog.safe_path(exam.get("bank", ""))
            bank = json.loads(bank_path.read_text(encoding="utf-8"))
            if bank.get("schema_version") != 1:
                errors.append(f"{exam.get('id')}: unsupported exam bank schema")
            questions = bank.get("questions")
            if not isinstance(questions, list) or not questions:
                errors.append(f"{exam.get('id')}: exam bank needs questions")
                continue
            for index, question in enumerate(questions, start=1):
                if not isinstance(question, dict):
                    errors.append(f"{exam.get('id')} question {index}: must be an object")
                    continue
                choices = question.get("choices")
                if not isinstance(choices, dict) or set(choices) != {"A", "B", "C", "D"}:
                    errors.append(f"{exam.get('id')} question {index}: choices must be A-D")
                if question.get("answer") not in {"A", "B", "C", "D"}:
                    errors.append(f"{exam.get('id')} question {index}: invalid answer")
                for field in ("prompt", "explanation"):
                    if not isinstance(question.get(field), str) or not question[field].strip():
                        errors.append(f"{exam.get('id')} question {index}: missing {field}")
        except (CourseError, FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(f"{exam.get('id')}: invalid exam bank: {exc}")

    references_path = catalog.root / "course" / "references.json"
    try:
        references = json.loads(references_path.read_text(encoding="utf-8"))
        if not isinstance(references, dict):
            errors.append("course/references.json: top level must be an object")
            references = {}
        if references.get("schema_version") != 1:
            errors.append("course/references.json: unsupported schema")
        verified_on = references.get("verified_on")
        verified_date: date | None = None
        if not isinstance(verified_on, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}", verified_on
        ):
            errors.append(
                "course/references.json: verified_on must be a real YYYY-MM-DD date"
            )
        else:
            try:
                verified_date = date.fromisoformat(verified_on)
            except ValueError:
                errors.append(
                    "course/references.json: verified_on must be a real YYYY-MM-DD date"
                )
        if verified_date is not None and verified_date > date.today():
            errors.append("course/references.json: verified_on cannot be in the future")
        mappings = references.get("items")
        if not isinstance(mappings, dict):
            errors.append("course/references.json: items must be an object")
            mappings = {}
        expected_items = set(module_ids) | {"capstone"}
        if set(mappings) != expected_items:
            errors.append(
                "external-source coverage mismatch: "
                f"missing={sorted(expected_items - set(mappings))}, "
                f"extra={sorted(set(mappings) - expected_items)}"
            )
        reference_pages: dict[str, Path] = {}
        for module in modules:
            item_id = module.get("id")
            if not isinstance(item_id, str):
                continue
            try:
                reference_pages[item_id] = catalog.safe_path(module.get("path", ""))
            except (CourseError, TypeError):
                # The catalog-page pass above already records the path error.
                continue
        reference_pages["capstone"] = catalog.root / "vault" / "Capstone - Browser in a Box.md"
        all_urls: set[str] = set()
        for item_id, entries in mappings.items():
            if not isinstance(entries, list) or not 2 <= len(entries) <= 4:
                errors.append(f"{item_id}: expected 2 to 4 external sources")
                continue
            local_urls: set[str] = set()
            has_start = False
            for index, entry in enumerate(entries, start=1):
                if not isinstance(entry, dict):
                    errors.append(f"{item_id} source {index}: must be an object")
                    continue
                for field in ("title", "url", "kind", "tier", "use"):
                    if not isinstance(entry.get(field), str) or not entry[field].strip():
                        errors.append(f"{item_id} source {index}: missing {field}")
                url = entry.get("url")
                if isinstance(url, str) and url:
                    if not url.startswith("https://"):
                        errors.append(f"{item_id} source {index}: URL must use HTTPS")
                    if url in local_urls:
                        errors.append(f"{item_id}: duplicate external URL {url}")
                    local_urls.add(url)
                    all_urls.add(url)
                if entry.get("kind") not in REFERENCE_KINDS:
                    errors.append(f"{item_id} source {index}: invalid kind")
                if entry.get("tier") not in REFERENCE_TIERS:
                    errors.append(f"{item_id} source {index}: invalid tier")
                has_start = has_start or entry.get("tier") == "start"
            if not has_start:
                errors.append(f"{item_id}: external sources need a Start here item")
            page = reference_pages.get(item_id)
            if page is None or not page.is_file():
                errors.append(f"{item_id}: missing referenced learning page")
                continue
            page_text = page.read_text(encoding="utf-8")
            start_count = page_text.count(REFERENCE_START)
            end_count = page_text.count(REFERENCE_END)
            headings = list(re.finditer(r"(?m)^## External sources$", page_text))
            if start_count != 1 or end_count != 1 or len(headings) != 1:
                errors.append(
                    f"{item_id}: external-source block needs exactly one heading "
                    "and one marker pair"
                )
            else:
                marker_start = page_text.index(REFERENCE_START)
                marker_end = page_text.index(REFERENCE_END)
                if not headings[0].end() < marker_start < marker_end:
                    errors.append(
                        f"{item_id}: external-source heading and markers are out of order"
                    )
            for url in local_urls:
                if url not in page_text:
                    errors.append(f"{item_id}: rendered page is missing {url}")
        shelf = catalog.root / "vault" / "Reference Shelf.md"
        if not shelf.is_file():
            errors.append("missing vault/Reference Shelf.md")
        else:
            shelf_text = shelf.read_text(encoding="utf-8")
            for url in all_urls:
                if url not in shelf_text:
                    errors.append(f"Reference Shelf is missing {url}")
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"invalid course/references.json: {exc}")

    # Check wiki links whose target is a vault page (anchors and aliases allowed).
    vault = catalog.root / "vault"
    stems = {path.stem for path in vault.rglob("*.md")} if vault.is_dir() else set()
    link_pattern = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
    if vault.is_dir():
        for path in vault.rglob("*.md"):
            for target in link_pattern.findall(path.read_text(encoding="utf-8")):
                cleaned = target.strip()
                target_path = Path(cleaned)
                if "/" in cleaned:
                    candidate = vault / target_path
                    if candidate.suffix.lower() != ".md":
                        candidate = candidate.with_suffix(".md")
                    resolved = candidate.is_file()
                else:
                    resolved = target_path.name in stems
                if not resolved:
                    errors.append(
                        f"{path.relative_to(catalog.root)}: broken wiki link [[{target}]]"
                    )

    try:
        challenge_catalog = ChallengeCatalog.load(catalog.root)
        errors.extend(validate_challenges(catalog, challenge_catalog))
    except CourseError as exc:
        errors.append(str(exc))
    return errors

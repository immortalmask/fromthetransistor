#!/usr/bin/env python3
"""Render curated external references into module pages and the vault shelf."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "course" / "catalog.json"
REFERENCES_PATH = ROOT / "course" / "references.json"
SHELF_PATH = ROOT / "vault" / "Reference Shelf.md"
START_MARKER = "<!-- ftt:references:start -->"
END_MARKER = "<!-- ftt:references:end -->"
TIERS = {"start": "Start here", "reference": "Reference", "deeper": "Go deeper"}
KINDS = {
    "course": "Course",
    "manual": "Manual",
    "specification": "Specification",
    "project": "Project",
    "paper": "Paper",
    "datasheet": "Datasheet",
}


class ReferenceError(RuntimeError):
    pass


def load_data() -> tuple[dict[str, Any], dict[str, Any]]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    references = json.loads(REFERENCES_PATH.read_text(encoding="utf-8"))
    if not isinstance(catalog, dict):
        raise ReferenceError("course/catalog.json must contain an object")
    if not isinstance(references, dict):
        raise ReferenceError("course/references.json must contain an object")
    if references.get("schema_version") != 1:
        raise ReferenceError("course/references.json must use schema_version 1")
    return catalog, references


def safe_repo_path(relative: Any, label: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ReferenceError(f"{label}: path must be a non-empty string")
    candidate = Path(relative)
    if candidate.is_absolute():
        raise ReferenceError(f"{label}: path must be relative: {relative}")
    resolved = (ROOT / candidate).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ReferenceError(f"{label}: path escapes repository: {relative}") from exc
    return resolved


def page_map(catalog: dict[str, Any]) -> dict[str, tuple[Path, str]]:
    modules = catalog.get("modules")
    if not isinstance(modules, list):
        raise ReferenceError("course/catalog.json: modules must be an array")
    pages: dict[str, tuple[Path, str]] = {}
    owners: dict[Path, str] = {}
    for index, module in enumerate(modules, start=1):
        if not isinstance(module, dict):
            raise ReferenceError(f"catalog module {index}: must be an object")
        item_id = module.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            raise ReferenceError(f"catalog module {index}: missing id")
        if item_id in pages:
            raise ReferenceError(f"duplicate catalog module id: {item_id}")
        path = safe_repo_path(module.get("path"), item_id)
        if path in owners:
            raise ReferenceError(
                f"catalog modules {owners[path]} and {item_id} share page {path.relative_to(ROOT)}"
            )
        owners[path] = item_id
        pages[item_id] = (path, path.stem)

    if "capstone" in pages:
        raise ReferenceError("catalog module id 'capstone' is reserved")
    capstone_path = safe_repo_path(
        "vault/Capstone - Browser in a Box.md", "capstone"
    )
    if capstone_path in owners:
        raise ReferenceError(
            f"catalog module {owners[capstone_path]} shares the capstone page"
        )
    pages["capstone"] = (
        capstone_path,
        "Capstone - Browser in a Box",
    )
    return pages


def validate_data(catalog: dict[str, Any], references: dict[str, Any]) -> None:
    verified_on = references.get("verified_on")
    if not isinstance(verified_on, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}", verified_on
    ):
        raise ReferenceError("verified_on must be a real YYYY-MM-DD date")
    try:
        verified_date = date.fromisoformat(verified_on)
    except ValueError as exc:
        raise ReferenceError("verified_on must be a real YYYY-MM-DD date") from exc
    if verified_date > date.today():
        raise ReferenceError("verified_on cannot be in the future")

    pages = page_map(catalog)
    mappings = references.get("items")
    if not isinstance(mappings, dict):
        raise ReferenceError("references.items must be an object")
    missing = set(pages) - set(mappings)
    extra = set(mappings) - set(pages)
    if missing or extra:
        raise ReferenceError(
            f"reference coverage mismatch: missing={sorted(missing)}, extra={sorted(extra)}"
        )
    for item_id, entries in mappings.items():
        if not isinstance(entries, list) or not 2 <= len(entries) <= 4:
            raise ReferenceError(f"{item_id}: expected 2 to 4 external sources")
        urls: set[str] = set()
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                raise ReferenceError(f"{item_id} source {index}: must be an object")
            for field in ("title", "url", "kind", "tier", "use"):
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    raise ReferenceError(f"{item_id} source {index}: missing {field}")
            if entry["kind"] not in KINDS:
                raise ReferenceError(f"{item_id} source {index}: invalid kind")
            if entry["tier"] not in TIERS:
                raise ReferenceError(f"{item_id} source {index}: invalid tier")
            if not entry["url"].startswith("https://"):
                raise ReferenceError(f"{item_id} source {index}: URL must use HTTPS")
            if entry["url"] in urls:
                raise ReferenceError(f"{item_id}: duplicate URL {entry['url']}")
            urls.add(entry["url"])
        if not any(entry["tier"] == "start" for entry in entries):
            raise ReferenceError(f"{item_id}: at least one source must be Start here")


def render_entries(entries: list[dict[str, str]]) -> str:
    lines = [
        "## External sources",
        "",
        "Use these for the named task; specifications are lookup material, not cover-to-cover reading.",
        "",
        START_MARKER,
    ]
    for entry in entries:
        label = f"{TIERS[entry['tier']]} · {KINDS[entry['kind']]}"
        lines.append(
            f"- **{label}:** [{entry['title']}]({entry['url']}) — {entry['use']}"
        )
    lines.extend([END_MARKER, "", ""])
    return "\n".join(lines)


def replace_block(text: str, block: str, insertion_heading: str, path: Path) -> str:
    external_headings = list(re.finditer(r"(?m)^## External sources$", text))
    start_count = text.count(START_MARKER)
    end_count = text.count(END_MARKER)

    if start_count == 0 and end_count == 0:
        if external_headings:
            raise ReferenceError(
                f"{path}: External sources heading exists without generated markers"
            )
        insertion_headings = list(
            re.finditer(rf"(?m)^{re.escape(insertion_heading)}$", text)
        )
        if len(insertion_headings) != 1:
            raise ReferenceError(
                f"{path}: expected exactly one insertion heading {insertion_heading}"
            )
        insertion_start = insertion_headings[0].start()
        return text[:insertion_start] + block + text[insertion_start:]

    if start_count != 1 or end_count != 1:
        raise ReferenceError(
            f"{path}: expected exactly one ordered reference marker pair"
        )
    if len(external_headings) != 1:
        raise ReferenceError(
            f"{path}: generated markers require exactly one External sources heading"
        )

    marker_start = text.index(START_MARKER)
    marker_end_start = text.index(END_MARKER)
    marker_end = marker_end_start + len(END_MARKER)
    section_heading = external_headings[0]
    if not section_heading.end() < marker_start < marker_end_start:
        raise ReferenceError(f"{path}: reference heading and markers are out of order")
    if re.search(r"(?m)^## .+$", text[section_heading.end() : marker_start]):
        raise ReferenceError(f"{path}: reference marker is outside its section")
    if re.search(r"(?m)^## .+$", text[marker_start:marker_end_start]):
        raise ReferenceError(f"{path}: level-two heading appears inside reference markers")

    next_heading = re.search(r"(?m)^## .+$", text[marker_end:])
    if next_heading is None:
        raise ReferenceError(f"{path}: reference section has no following heading")
    following_heading = next_heading.group(0)
    if following_heading != insertion_heading:
        raise ReferenceError(
            f"{path}: reference section must precede {insertion_heading}, "
            f"found {following_heading}"
        )
    following_start = marker_end + next_heading.start()
    return text[: section_heading.start()] + block + text[following_start:]


def desired_pages(
    catalog: dict[str, Any], references: dict[str, Any]
) -> dict[Path, str]:
    desired: dict[Path, str] = {}
    for item_id, (path, _stem) in page_map(catalog).items():
        text = path.read_text(encoding="utf-8")
        insertion = "## Stretch ladder" if item_id == "capstone" else "## Exit criteria"
        desired[path] = replace_block(
            text, render_entries(references["items"][item_id]), insertion, path
        )
    return desired


def render_shelf(catalog: dict[str, Any], references: dict[str, Any]) -> str:
    lines = [
        "---",
        'title: "Reference Shelf"',
        'tags: ["ftt", "references", "sources"]',
        "---",
        "",
        "# Reference Shelf",
        "",
        f"Links last verified: {references['verified_on']}.",
        "",
        "This shelf mirrors each module's short source list. **Start here** items are",
        "the approachable entry point; **Reference** items answer exact contract questions;",
        "**Go deeper** items are for comparison or extension. Read only the portion named",
        "by the task. A specification is rarely the best first explanation.",
        "",
        "See [[Scope Decisions]] for the boundary between the software core and optional",
        "hardware work.",
        "",
    ]
    for section in catalog["sections"]:
        lines.extend([f"## {section['id']} — {section['title']}", ""])
        for module in catalog["modules"]:
            if module["section"] != section["id"]:
                continue
            stem = Path(module["path"]).stem
            lines.extend([f"### [[{stem}]]", ""])
            for entry in references["items"][module["id"]]:
                label = f"{TIERS[entry['tier']]} · {KINDS[entry['kind']]}"
                lines.append(
                    f"- **{label}:** [{entry['title']}]({entry['url']}) — {entry['use']}"
                )
            lines.append("")
    lines.extend(["## Capstone", "", "### [[Capstone - Browser in a Box]]", ""])
    for entry in references["items"]["capstone"]:
        label = f"{TIERS[entry['tier']]} · {KINDS[entry['kind']]}"
        lines.append(
            f"- **{label}:** [{entry['title']}]({entry['url']}) — {entry['use']}"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="fail when rendered pages are out of date"
    )
    args = parser.parse_args()
    try:
        catalog, references = load_data()
        validate_data(catalog, references)
        pages = desired_pages(catalog, references)
        pages[SHELF_PATH] = render_shelf(catalog, references)
    except (OSError, json.JSONDecodeError, ReferenceError, KeyError, TypeError) as exc:
        print(f"reference error: {exc}", file=sys.stderr)
        return 1

    stale = [
        path
        for path, desired in pages.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != desired
    ]
    if args.check:
        if stale:
            for path in stale:
                print(f"stale: {path.relative_to(ROOT)}")
            return 1
        print(f"PASS: {len(pages) - 1} referenced learning pages and Reference Shelf are synced")
        return 0
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(pages[path], encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
    if not stale:
        print("Reference pages already synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

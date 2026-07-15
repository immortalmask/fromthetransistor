#!/usr/bin/env python3
"""Render the hard-problem track from course/challenges.json."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ftt.challenges import ChallengeCatalog, render_atlas, render_pack  # noqa: E402
from ftt.model import Catalog, CourseError  # noqa: E402


def expected_pages(catalog: ChallengeCatalog) -> dict[Path, str]:
    course = Catalog.load(catalog.root)
    challenge_root = (catalog.root / "vault" / "Challenges").resolve()
    atlas = (catalog.root / "vault" / "Challenge Atlas.md").resolve()
    pages: dict[Path, str] = {}
    for pack in catalog.packs:
        path = course.safe_path(pack["path"])
        if path.parent != challenge_root or path.suffix != ".md":
            raise CourseError(
                f"{pack.get('id')}: generated page must be directly under vault/Challenges"
            )
        if path == atlas or path in pages:
            raise CourseError(f"duplicate or reserved generated page: {path}")
        pages[path] = render_pack(pack)
    if atlas in pages:
        raise CourseError(f"duplicate generated atlas page: {atlas}")
    pages[atlas] = render_atlas(catalog)
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="reject stale rendered pages")
    args = parser.parse_args()
    try:
        catalog = ChallengeCatalog.load(ROOT)
        pages = expected_pages(catalog)
        stale: list[Path] = []
        for path, expected in pages.items():
            expected = expected.rstrip() + "\n"
            if args.check:
                try:
                    current = path.read_text(encoding="utf-8")
                except FileNotFoundError:
                    current = ""
                if current != expected:
                    stale.append(path)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8")
                print(f"wrote {path.relative_to(ROOT)}")
        if stale:
            for path in stale:
                print(f"stale: {path.relative_to(ROOT)}", file=sys.stderr)
            print("run: python3 tools/sync_challenges.py", file=sys.stderr)
            return 1
        if args.check:
            print(f"PASS: {len(pages)} hard-track pages are synchronized")
        return 0
    except CourseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

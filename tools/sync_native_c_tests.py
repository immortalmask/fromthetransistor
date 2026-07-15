#!/usr/bin/env python3
"""Render each lab.json behavioral contract as a co-located native C suite."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ftt.model import Catalog, CourseError  # noqa: E402
from ftt.runner import validate_lab_spec  # noqa: E402


def c_string(value: str) -> str:
    """Return an ASCII C literal whose bytes equal value encoded as UTF-8."""

    pieces: list[str] = ['"']
    for byte in value.encode("utf-8"):
        if byte == 0x22:
            pieces.append(r'\"')
        elif byte == 0x5C:
            pieces.append(r"\\")
        elif byte == 0x0A:
            pieces.append(r"\n")
        elif byte == 0x0D:
            pieces.append(r"\r")
        elif byte == 0x09:
            pieces.append(r"\t")
        elif 0x20 <= byte <= 0x7E:
            pieces.append(chr(byte))
        else:
            pieces.append(f"\\{byte:03o}")
    pieces.append('"')
    return "".join(pieces)


def render_case(index: int, case: dict[str, Any]) -> str:
    mode = {
        "exact": "CTEST_EXACT",
        "contains": "CTEST_CONTAINS",
    }[case.get("stdout_mode", "exact")]
    return "\n".join(
        [
            "    CTEST_CASE(",
            f"        {c_string(case['name'])},",
            f"        ARGS_{index:02d},",
            f"        {c_string(case.get('stdin', ''))},",
            f"        {int(case.get('expected_exit', 0))},",
            f"        {c_string(case.get('expected_stdout', ''))},",
            f"        {mode}),",
        ]
    )


def render(spec: dict[str, Any]) -> str:
    lines = [
        "/* Generated from lab.json by tools/sync_native_c_tests.py. */",
        '#include "test_support.h"',
        "",
    ]
    for index, case in enumerate(spec["tests"], start=1):
        argv = case["argv"]
        if not argv or argv[0] != "{build}/program":
            raise CourseError(
                f"{spec['id']} case {case['name']}: first argv must be {{build}}/program"
            )
        arguments = ", ".join(c_string(value) for value in argv[1:])
        if arguments:
            arguments += ", "
        lines.append(
            f"static const char *const ARGS_{index:02d}[] = "
            f"{{{arguments}NULL}};"
        )
    lines.extend(["", "static const struct ctest_case CASES[] = {"])
    for index, case in enumerate(spec["tests"], start=1):
        lines.append(render_case(index, case))
    lines.extend(
        [
            "};",
            "",
            "int main(int argc, char **argv) {",
            "    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));",
            "}",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if any checked-in native suite differs from lab.json",
    )
    args = parser.parse_args(argv)

    catalog = Catalog.load(ROOT)
    labs = [module["lab"] for module in catalog.modules if module.get("lab")]
    mismatches: list[Path] = []
    for lab_id in labs:
        spec = validate_lab_spec(catalog.lab_spec(lab_id), expected_id=lab_id)
        expected = render(spec)
        destination = ROOT / "labs" / lab_id / "tests" / "test.c"
        if args.check:
            try:
                actual = destination.read_text(encoding="utf-8")
            except FileNotFoundError:
                actual = ""
            if actual != expected:
                mismatches.append(destination.relative_to(ROOT))
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(expected, encoding="utf-8")
        print(f"rendered {destination.relative_to(ROOT)} ({len(spec['tests'])} cases)")

    if mismatches:
        for path in mismatches:
            print(f"OUT OF SYNC: {path}", file=sys.stderr)
        print(
            "Run python3 tools/sync_native_c_tests.py to regenerate native suites.",
            file=sys.stderr,
        )
        return 1
    if args.check:
        print(f"PASS: {len(labs)} native C suites are synchronized with lab.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

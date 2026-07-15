"""Command-line interface for the executable course."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import sys
from typing import Sequence

from . import __version__
from .challenges import (
    ChallengeCatalog,
    check_evidence,
    render_challenge_brief,
    start_challenge,
)
from .model import Catalog, CourseError, find_root
from .progress import ProgressStore
from .runner import LabResult, run_lab, start_lab
from .validation import validate


def _catalog(args: argparse.Namespace) -> Catalog:
    return Catalog.load(find_root(args.root))


def _challenge_catalog(args: argparse.Namespace) -> ChallengeCatalog:
    root = find_root(args.root)
    return ChallengeCatalog.load(root)


def _workspace_root(catalog: Catalog) -> Path:
    return Path(os.environ.get("FTT_WORK_DIR", catalog.root / "work")).expanduser()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _challenge_evidence_current(entry: object) -> bool:
    if not isinstance(entry, dict):
        return False
    evidence = entry.get("evidence")
    expected = entry.get("evidence_digest")
    if not isinstance(evidence, str) or not isinstance(expected, str):
        return False
    try:
        path = Path(evidence).expanduser()
        return path.is_file() and _file_sha256(path) == expected
    except OSError:
        return False


def _render_result(result: LabResult) -> None:
    print(f"build  {'PASS' if result.build_passed else 'FAIL'}")
    if result.build_output and not result.build_passed:
        print(result.build_output.rstrip())
    for case in result.cases:
        print(f"test   {'PASS' if case.passed else 'FAIL'}  {case.name}")
        if case.detail:
            for line in case.detail.rstrip().splitlines():
                print(f"       {line}")
    passed = sum(case.passed for case in result.cases)
    print(f"result {'PASS' if result.passed else 'FAIL'}  {passed}/{len(result.cases)} tests")


def cmd_doctor(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    rows = []
    for tool in catalog.toolchain:
        location = shutil.which(tool["command"])
        rows.append({**tool, "available": bool(location), "path": location})
    errors = validate(catalog)
    if args.json:
        print(json.dumps({"tools": rows, "validation_errors": errors}, indent=2))
    else:
        print("Course structure")
        print(f"  {'PASS' if not errors else 'FAIL'}  {len(errors)} validation error(s)")
        for error in errors:
            print(f"        {error}")
        print("Toolchain")
        for row in rows:
            status = "PASS" if row["available"] else "MISS"
            required = "required" if row.get("required") else "optional"
            detail = row["path"] or row.get("install_hint", "not found")
            print(f"  {status}  {row['command']:<18} {required:<8} {detail}")
    missing = [row for row in rows if row.get("required") and not row["available"]]
    return 1 if errors or missing else 0


def cmd_validate(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    errors = validate(catalog)
    if errors:
        print(f"FAIL: {len(errors)} course validation error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    source_count = len([m for m in catalog.modules if m.get("source_ref")])
    lab_count = len([m for m in catalog.modules if m.get("lab")])
    challenge_count = len(ChallengeCatalog.load(catalog.root).challenges)
    print(
        f"PASS: {len(catalog.sections)} sections, {len(catalog.modules)} modules, "
        f"{source_count} source blocks, {lab_count} labs, {len(catalog.exams)} exams, "
        f"{challenge_count} hard problems"
    )
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    completed = ProgressStore(catalog.root).read()["modules"]
    sections = catalog.sections
    if args.section:
        selected = catalog.section(args.section)
        sections = [selected]
    for section in sections:
        print(f"\n{section['id']}  {section['title']}  ({section['weeks']})")
        for module in catalog.modules:
            if module["section"] != section["id"]:
                continue
            marker = "x" if module["id"] in completed else " "
            lab = f" lab:{module['lab']}" if module.get("lab") else ""
            optional = " optional" if module.get("optional") else ""
            print(
                f"  [{marker}] {module['id']:<5} {module['title']}"
                f"  ~{module['duration_hours']}h{lab}{optional}"
            )
    print()
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    try:
        item = catalog.module(args.target)
    except CourseError:
        item = catalog.exam(args.target)
    path = catalog.page_path(item)
    if args.path:
        print(path)
    else:
        print(path.read_text(encoding="utf-8"), end="")
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    completed = set(ProgressStore(catalog.root).read()["modules"])
    blocked: list[dict[str, object]] = []
    for module in catalog.modules:
        if module["id"] in completed or module.get("optional"):
            continue
        missing = [p for p in module.get("prerequisites", []) if p not in completed]
        if not missing:
            print(f"{module['id']}  {module['title']}")
            print(catalog.page_path(module))
            return 0
        blocked.append({"module": module, "missing": missing})
    if blocked:
        first = blocked[0]
        module = first["module"]
        print(f"No module is currently unlocked. {module['id']} needs: {', '.join(first['missing'])}")
        return 1
    print("All required modules are complete.")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    lab_id = catalog.lab_id(args.target)
    destination = (
        Path(args.dest)
        if args.dest
        else _workspace_root(catalog) / lab_id
    )
    created = start_lab(catalog, lab_id, destination, force=args.force)
    print(f"Started {lab_id} at {created}")
    print(f"Next: python3 ftt check {lab_id}")
    print(f"Native C tests: cd {created} && make test")
    return 0


def _check_one(
    catalog: Catalog,
    target: str,
    work: Path | None,
    solution: bool,
    record: bool,
) -> bool:
    lab_id = catalog.lab_id(target)
    spec = catalog.lab_spec(lab_id)
    if solution:
        work = catalog.root / "labs" / lab_id / "solution"
    elif work is None:
        work = _workspace_root(catalog) / lab_id
    result = run_lab(catalog, lab_id, work)
    print(f"\n{lab_id} — {spec['title']}")
    _render_result(result)
    if record and not solution:
        store = ProgressStore(catalog.root)
        store.record_lab(lab_id, result.passed, len(result.cases))
        if result.passed:
            store.mark_module(
                spec["module"],
                evidence=f"Automated lab {lab_id}: {len(result.cases)} tests passed",
                source="lab-check",
            )
    return result.passed


def cmd_check(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    if args.all_solutions:
        lab_ids = [m["lab"] for m in catalog.modules if m.get("lab")]
        outcomes = [
            _check_one(catalog, lab_id, None, solution=True, record=False)
            for lab_id in lab_ids
        ]
        print(f"\nsolutions: {sum(outcomes)}/{len(outcomes)} passed")
        return 0 if all(outcomes) else 1
    if args.all:
        lab_ids = [m["lab"] for m in catalog.modules if m.get("lab")]
        outcomes: list[bool] = []
        for lab_id in lab_ids:
            workspace = _workspace_root(catalog) / lab_id
            if not workspace.is_dir():
                print(f"\n{lab_id}\nresult MISS  workspace not started: {workspace}")
                outcomes.append(False)
                continue
            outcomes.append(
                _check_one(catalog, lab_id, workspace, solution=False, record=True)
            )
        print(f"\nlearner labs: {sum(outcomes)}/{len(outcomes)} passed")
        return 0 if all(outcomes) else 1
    if not args.target:
        raise CourseError("check needs a module/lab id or --all-solutions")
    passed = _check_one(
        catalog,
        args.target,
        Path(args.work) if args.work else None,
        solution=args.solution,
        record=not args.no_record,
    )
    return 0 if passed else 1


def cmd_complete(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    module = catalog.module(args.target)
    store = ProgressStore(catalog.root)
    if args.undo:
        store.unmark_module(module["id"])
        print(f"Marked {module['id']} incomplete")
        return 0
    if not args.evidence:
        raise CourseError("Manual completion requires --evidence describing what you produced")
    store.mark_module(module["id"], args.evidence, source="manual")
    print(f"Completed {module['id']}: {module['title']}")
    return 0


def cmd_progress(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    challenge_catalog = ChallengeCatalog.load(catalog.root)
    data = ProgressStore(catalog.root).read()
    completed = data["modules"]
    required = [m for m in catalog.modules if not m.get("optional")]
    done = [m for m in required if m["id"] in completed]
    challenge_entries = data.get("challenges", {})
    current_challenges = {
        challenge_id: entry
        for challenge_id, entry in challenge_entries.items()
        if _challenge_evidence_current(entry)
    }
    payload = {
        "completed": len(done),
        "required": len(required),
        "percent": round(100 * len(done) / len(required), 1) if required else 100.0,
        "modules": data["modules"],
        "labs": data["labs"],
        "challenges": data.get("challenges", {}),
        "hard_track_completed": len(current_challenges),
        "hard_track_stale": len(challenge_entries) - len(current_challenges),
        "hard_track_total": len(challenge_catalog.challenges),
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    print(f"Progress: {payload['completed']}/{payload['required']} required modules ({payload['percent']}%)")
    for section in catalog.sections:
        modules = [m for m in required if m["section"] == section["id"]]
        section_done = sum(m["id"] in completed for m in modules)
        print(f"  {section['id']}  {section_done}/{len(modules)}  {section['title']}")
    print(
        f"Hard track: {payload['hard_track_completed']}/{payload['hard_track_total']} "
        "replayable evidence packets"
    )
    if payload["hard_track_stale"]:
        print(f"  STALE  {payload['hard_track_stale']} recorded packet(s) changed or disappeared")
    if completed:
        print("\nEvidence")
        for module in catalog.modules:
            if module["id"] in completed:
                entry = completed[module["id"]]
                print(f"  {module['id']}  {entry['evidence']}")
    if data.get("challenges"):
        print("\nHard-track evidence")
        for challenge_id, entry in sorted(data["challenges"].items()):
            print(f"  {challenge_id}  {entry['evidence']}")
    return 0


def _exam_questions(catalog: Catalog, exam: dict[str, object]) -> list[dict[str, object]]:
    path = catalog.root / str(exam["bank"])
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise CourseError(f"Unsupported exam bank schema: {path}")
    return data["questions"]


def cmd_exam(args: argparse.Namespace) -> int:
    catalog = _catalog(args)
    if args.target == "list":
        for exam in catalog.exams:
            print(f"{exam['id']:<10} {exam['title']}  pass:{exam['passing_percent']}%")
        return 0
    exam = catalog.exam(args.target)
    questions = _exam_questions(catalog, exam)
    if not args.answers:
        print(f"{exam['title']} — {len(questions)} automatically graded questions")
        print(f"Practical: {catalog.root / exam['path']}")
        for number, question in enumerate(questions, start=1):
            print(f"\n{number}. {question['prompt']}")
            for key, choice in question["choices"].items():
                print(f"   {key}. {choice}")
        print(f"\nGrade with: python3 ftt exam {exam['id']} --answers A,B,...")
        return 0

    answers = [value.strip().upper() for value in args.answers.split(",")]
    if len(answers) != len(questions):
        raise CourseError(f"Expected {len(questions)} comma-separated answers, got {len(answers)}")
    correct = 0
    for number, (question, answer) in enumerate(zip(questions, answers), start=1):
        expected = question["answer"]
        passed = answer == expected
        correct += passed
        print(f"{number}. {'PASS' if passed else 'MISS'}  yours:{answer} expected:{expected}")
        if args.reveal or not passed:
            print(f"   {question['explanation']}")
    percent = round(100 * correct / len(questions))
    passed = percent >= int(exam["passing_percent"])
    print(f"score: {correct}/{len(questions)} ({percent}%) — {'PASS' if passed else 'REVIEW'}")
    print("The practical investigation in the exam page is graded with its rubric, separately.")
    return 0 if passed else 1


def cmd_challenge(args: argparse.Namespace) -> int:
    catalog = _challenge_catalog(args)
    action = args.challenge_action
    if action == "list":
        completed = ProgressStore(catalog.root).read().get("challenges", {})
        packs = catalog.packs
        if args.stage:
            packs = [catalog.pack(args.stage)]
        for pack in packs:
            print(f"\n{pack['id']}  {pack['title']}")
            for challenge in pack["challenges"]:
                entry = completed.get(challenge["id"])
                marker = "x" if _challenge_evidence_current(entry) else "!" if entry else " "
                stars = "*" * int(challenge["stars"])
                print(
                    f"  [{marker}] {challenge['id']:<6} {stars:<3} {challenge['title']}  "
                    f"~{challenge['estimated_hours']}h {challenge['difficulty']}"
                )
        print()
        if any(not _challenge_evidence_current(entry) for entry in completed.values()):
            print("[!] recorded evidence changed or disappeared; replay it before relying on completion.\n")
        return 0

    challenge = catalog.challenge(args.target)
    progress = ProgressStore(catalog.root).read()
    satisfied = set(progress["modules"]) | set(progress.get("challenges", {}))
    missing = [
        requirement
        for requirement in challenge.get("prerequisites", [])
        if requirement not in satisfied
    ]
    if action == "show":
        if args.path:
            pack = catalog.challenge_pack(challenge["id"])
            print(catalog.safe_path(pack["path"]))
        else:
            pack = catalog.challenge_pack(challenge["id"])
            print(render_challenge_brief(challenge, pack), end="")
        if missing and not args.path:
            print(f"\nLOCKED guidance: complete or consciously waive {', '.join(missing)}")
        return 0

    destination = (
        Path(args.work)
        if args.work
        else _workspace_root(Catalog.load(catalog.root)) / "challenges" / challenge["id"]
    )
    if action == "start":
        if missing:
            print(
                f"WARNING: unmet prerequisites: {', '.join(missing)}. "
                "Workspace creation is allowed for inspection."
            )
        created = start_challenge(catalog, challenge["id"], destination, force=args.force)
        print(f"Started {challenge['id']} at {created}")
        print(f"Read {created / 'CHALLENGE.md'} and fill evidence.json as you work.")
        replay = f"python3 ftt challenge check {challenge['id']}"
        if args.work:
            replay += f" --work {shlex.quote(str(created))}"
        print(f"Replay with: {replay}")
        return 0

    if action == "check":
        result = check_evidence(catalog, challenge["id"], destination)
        print(f"\n{challenge['id']} — {challenge['title']}")
        for error in result.errors:
            print(f"packet FAIL  {error}")
        for replay in result.replays:
            print(f"replay {'PASS' if replay.passed else 'FAIL'}  {replay.name}")
            if replay.detail:
                print(f"       {replay.detail}")
        print(
            f"result {'PASS' if result.passed else 'FAIL'}  "
            f"{sum(replay.passed for replay in result.replays)}/{len(result.replays)} replays"
        )
        if result.passed and not args.no_record:
            if missing and not args.waive_prerequisites:
                print(
                    "completion BLOCKED  unmet prerequisites; pass "
                    "--waive-prerequisites to record an explicit out-of-order waiver"
                )
                return 1
            packet_path = (destination / "evidence.json").resolve()
            ProgressStore(catalog.root).mark_challenge(
                challenge["id"],
                evidence=str(packet_path),
                evidence_digest=_file_sha256(packet_path),
                waived_prerequisites=missing if args.waive_prerequisites else [],
            )
        return 0 if result.passed else 1

    raise CourseError(f"Unknown challenge action: {action}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ftt",
        description="Run the From the Transistor to the Web Browser course",
    )
    parser.add_argument("--root", help="repository root (normally auto-detected)")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="check course files and local tools")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    validate_parser = subparsers.add_parser("validate", help="validate authored course data")
    validate_parser.set_defaults(func=cmd_validate)

    listing = subparsers.add_parser("list", help="list the learning path")
    listing.add_argument("--section")
    listing.set_defaults(func=cmd_list)

    show = subparsers.add_parser("show", help="print a module or exam page")
    show.add_argument("target")
    show.add_argument("--path", action="store_true", help="print only its filesystem path")
    show.set_defaults(func=cmd_show)

    next_parser = subparsers.add_parser("next", help="show the next unlocked module")
    next_parser.set_defaults(func=cmd_next)

    start = subparsers.add_parser("start", help="copy a lab starter into learner work")
    start.add_argument("target", help="module id, module slug, or lab id")
    start.add_argument("--dest")
    start.add_argument("--force", action="store_true")
    start.set_defaults(func=cmd_start)

    check = subparsers.add_parser("check", help="build and test learner work")
    check.add_argument("target", nargs="?")
    check.add_argument("--work", help="custom learner workspace")
    check.add_argument("--solution", action="store_true", help="check the reference solution")
    check.add_argument("--all", action="store_true", help="check every learner lab workspace")
    check.add_argument("--all-solutions", action="store_true")
    check.add_argument("--no-record", action="store_true")
    check.set_defaults(func=cmd_check)

    complete = subparsers.add_parser("complete", help="record a non-lab module artifact")
    complete.add_argument("target")
    complete.add_argument("--evidence")
    complete.add_argument("--undo", action="store_true")
    complete.set_defaults(func=cmd_complete)

    progress = subparsers.add_parser("progress", help="show local progress and evidence")
    progress.add_argument("--json", action="store_true")
    progress.set_defaults(func=cmd_progress)

    exam = subparsers.add_parser("exam", help="show or grade an exam")
    exam.add_argument("target", help="exam id or 'list'")
    exam.add_argument("--answers", help="comma-separated answer keys")
    exam.add_argument("--reveal", action="store_true")
    exam.set_defaults(func=cmd_exam)

    challenge = subparsers.add_parser(
        "challenge", help="browse and verify the cumulative hard-problem track"
    )
    challenge_subparsers = challenge.add_subparsers(
        dest="challenge_action", required=True
    )
    challenge_list = challenge_subparsers.add_parser("list", help="list hard problems")
    challenge_list.add_argument("--stage")
    challenge_list.set_defaults(func=cmd_challenge)
    challenge_show = challenge_subparsers.add_parser("show", help="print one hard problem")
    challenge_show.add_argument("target")
    challenge_show.add_argument("--path", action="store_true")
    challenge_show.set_defaults(func=cmd_challenge)
    challenge_start = challenge_subparsers.add_parser(
        "start", help="create a challenge evidence workspace"
    )
    challenge_start.add_argument("target")
    challenge_start.add_argument("--work")
    challenge_start.add_argument("--force", action="store_true")
    challenge_start.set_defaults(func=cmd_challenge)
    challenge_check = challenge_subparsers.add_parser(
        "check", help="verify hashes and replay an evidence packet"
    )
    challenge_check.add_argument("target")
    challenge_check.add_argument("--work")
    challenge_check.add_argument("--no-record", action="store_true")
    challenge_check.add_argument(
        "--waive-prerequisites",
        action="store_true",
        help="record a passing packet out of order with an explicit waiver",
    )
    challenge_check.set_defaults(func=cmd_challenge)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except CourseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130

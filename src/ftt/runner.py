"""Safe-enough local lab orchestration: argv only, no shell evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
from typing import Any

from .model import Catalog, CourseError


MAX_OUTPUT_BYTES = 128 * 1024
MAX_STDIN_BYTES = 1024 * 1024
MAX_CASE_TIMEOUT = 300.0
CHALLENGE_MAX_OUTPUT_BYTES = 1024 * 1024
CHALLENGE_MAX_FILE_BYTES = 256 * 1024 * 1024
CHALLENGE_MAX_ADDRESS_SPACE = 4 * 1024 * 1024 * 1024
CHALLENGE_MAX_OPEN_FILES = 256
OUTPUT_TRUNCATED_MARKER = "[output truncated]"
PLACEHOLDER = re.compile(r"\{([a-zA-Z][a-zA-Z0-9_]*)\}")
ALLOWED_PLACEHOLDERS = {"root", "work", "build", "python", "cc"}


@dataclass
class CaseResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class LabResult:
    lab_id: str
    build_passed: bool
    cases: list[CaseResult] = field(default_factory=list)
    build_output: str = ""

    @property
    def passed(self) -> bool:
        return self.build_passed and bool(self.cases) and all(
            case.passed for case in self.cases
        )


def _valid_timeout(value: Any) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return 0 < float(value) <= MAX_CASE_TIMEOUT


def _validate_argv(argv: Any, context: str) -> None:
    if (
        not isinstance(argv, list)
        or not argv
        or any(not isinstance(value, str) for value in argv)
        or not argv[0]
    ):
        raise CourseError(
            f"{context}: argv must be an array of strings with a non-empty command"
        )
    unknown = {
        match.group(1)
        for value in argv
        for match in PLACEHOLDER.finditer(value)
        if match.group(1) not in ALLOWED_PLACEHOLDERS
    }
    if unknown:
        raise CourseError(f"{context}: unknown placeholders {sorted(unknown)}")


def validate_lab_spec(spec: Any, expected_id: str | None = None) -> dict[str, Any]:
    """Validate the executable contract used by validation and execution."""

    if not isinstance(spec, dict) or spec.get("schema_version") != 1:
        raise CourseError("lab specification must be a schema-version 1 object")
    for field in ("id", "module", "title"):
        if not isinstance(spec.get(field), str) or not spec[field].strip():
            raise CourseError(f"lab specification needs a non-empty {field}")
    if expected_id is not None and spec["id"] != expected_id:
        raise CourseError(
            f"Lab id mismatch: expected {expected_id!r}, found {spec['id']!r}"
        )

    build = spec.get("build")
    if build is not None:
        if not isinstance(build, dict):
            raise CourseError(f"{spec['id']} build must be an object")
        _validate_argv(build.get("argv"), f"{spec['id']} build")
        if "timeout" in build and not _valid_timeout(build["timeout"]):
            raise CourseError(
                f"{spec['id']} build timeout must be in (0, {MAX_CASE_TIMEOUT:g}]"
            )
        expected_exit = build.get("expected_exit", 0)
        if isinstance(expected_exit, bool) or not isinstance(expected_exit, int):
            raise CourseError(f"{spec['id']} build expected_exit must be an integer")

    tests = spec.get("tests")
    if not isinstance(tests, list) or len(tests) < 3:
        raise CourseError(f"{spec['id']}: expected at least three deterministic tests")
    names: set[str] = set()
    for index, case in enumerate(tests, start=1):
        context = f"{spec['id']} test {index}"
        if not isinstance(case, dict):
            raise CourseError(f"{context}: test must be an object")
        name = case.get("name", f"case-{index}")
        if not isinstance(name, str) or not name.strip():
            raise CourseError(f"{context}: name must be a non-empty string")
        if name in names:
            raise CourseError(f"{spec['id']}: duplicate test name {name!r}")
        names.add(name)
        _validate_argv(case.get("argv"), context)
        if "timeout" in case and not _valid_timeout(case["timeout"]):
            raise CourseError(
                f"{context}: timeout must be in (0, {MAX_CASE_TIMEOUT:g}]"
            )
        expected_exit = case.get("expected_exit", 0)
        if isinstance(expected_exit, bool) or not isinstance(expected_exit, int):
            raise CourseError(f"{context}: expected_exit must be an integer")
        for field in ("stdin", "expected_stdout"):
            value = case.get(field, "")
            if not isinstance(value, str):
                raise CourseError(f"{context}: {field} must be a string")
        if len(case.get("stdin", "").encode("utf-8")) > MAX_STDIN_BYTES:
            raise CourseError(
                f"{context}: stdin exceeds the {MAX_STDIN_BYTES}-byte fixture limit"
            )
        mode = case.get("stdout_mode", "exact")
        if mode not in {"exact", "contains"}:
            raise CourseError(f"{context}: stdout_mode must be exact or contains")
        if mode == "contains" and not case.get("expected_stdout", ""):
            raise CourseError(f"{context}: contains mode needs non-empty expected_stdout")
    return spec


def _expand(argv: list[str], values: dict[str, str]) -> list[str]:
    def replace(match: Any) -> str:
        key = match.group(1)
        try:
            return values[key]
        except KeyError as exc:
            raise CourseError(f"Unknown command placeholder: {key}") from exc

    return [PLACEHOLDER.sub(replace, value) for value in argv]


def _run(
    argv: list[str],
    cwd: Path,
    timeout: float,
    stdin: str = "",
    sandbox_home: Path | None = None,
    *,
    max_output_bytes: int = MAX_OUTPUT_BYTES,
    max_file_bytes: int = 16 * 1024 * 1024,
    max_address_space: int = 768 * 1024 * 1024,
    max_open_files: int = 64,
) -> subprocess.CompletedProcess[str]:
    sandbox_home = sandbox_home or cwd
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": str(sandbox_home),
        "TMPDIR": str(sandbox_home),
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "CCACHE_DISABLE": "1",
        "PYTHONHASHSEED": "0",
    }
    if os.name == "nt" and os.environ.get("SystemRoot"):
        env["SystemRoot"] = os.environ["SystemRoot"]

    def limit_resources() -> None:
        try:
            import resource

            limits = (
                ("RLIMIT_CORE", 0),
                ("RLIMIT_FSIZE", max_file_bytes),
                ("RLIMIT_NOFILE", max_open_files),
                ("RLIMIT_AS", max_address_space),
                ("RLIMIT_CPU", max(1, int(timeout) + 1)),
            )
            for name, value in limits:
                kind = getattr(resource, name, None)
                if kind is not None:
                    resource.setrlimit(kind, (value, value))
        except (ImportError, OSError, ValueError):
            # Wall-time enforcement still applies on platforms without POSIX rlimits.
            return

    process = subprocess.Popen(
        argv,
        cwd=cwd,
        text=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        start_new_session=(os.name == "posix"),
        preexec_fn=limit_resources if os.name == "posix" else None,
    )
    captured = bytearray()
    output_truncated = False

    def drain_output() -> None:
        nonlocal output_truncated
        assert process.stdout is not None
        try:
            while True:
                chunk = process.stdout.read(64 * 1024)
                if not chunk:
                    return
                remaining = max_output_bytes - len(captured)
                if remaining > 0:
                    captured.extend(chunk[:remaining])
                if len(chunk) > remaining:
                    output_truncated = True
        except (OSError, ValueError):
            return

    def feed_input() -> None:
        assert process.stdin is not None
        try:
            process.stdin.write(stdin.encode("utf-8"))
            process.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        finally:
            try:
                process.stdin.close()
            except OSError:
                pass

    reader = threading.Thread(target=drain_output, name="ftt-output-drain", daemon=True)
    writer = threading.Thread(target=feed_input, name="ftt-input-feed", daemon=True)
    reader.start()
    writer.start()
    timed_out = False
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
        except ProcessLookupError:
            pass
        process.wait()
    if os.name == "posix":
        # Do not let a replay/build leave children holding pipes or servers alive.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    writer.join()
    reader.join(timeout=1)
    if reader.is_alive() and process.stdout is not None:
        process.stdout.close()
        reader.join(timeout=1)
    if process.stdout is not None:
        process.stdout.close()
    output = bytes(captured).decode("utf-8", errors="replace")
    if output_truncated:
        output += f"\n{OUTPUT_TRUNCATED_MARKER}\n"
    if timed_out:
        raise subprocess.TimeoutExpired(argv, timeout, output=output)
    return subprocess.CompletedProcess(argv, process.returncode, output, None)


def run_argv_limited(
    argv: list[str], cwd: Path, timeout: float
) -> subprocess.CompletedProcess[str]:
    """Run one local argv with the course's output, process, and resource limits."""

    return _run(
        argv,
        cwd,
        timeout,
        stdin="",
        sandbox_home=cwd,
        max_output_bytes=CHALLENGE_MAX_OUTPUT_BYTES,
        max_file_bytes=CHALLENGE_MAX_FILE_BYTES,
        max_address_space=CHALLENGE_MAX_ADDRESS_SPACE,
        max_open_files=CHALLENGE_MAX_OPEN_FILES,
    )


def _normal(text: str) -> str:
    return text.replace("\r\n", "\n")


def run_lab(catalog: Catalog, lab_id: str, work: Path) -> LabResult:
    spec = validate_lab_spec(catalog.lab_spec(lab_id), expected_id=lab_id)
    work = work.expanduser().resolve()
    if not work.is_dir():
        raise CourseError(f"Lab workspace does not exist: {work}")

    with tempfile.TemporaryDirectory(prefix=f"ftt-{lab_id}-") as temporary:
        build = Path(temporary)
        values = {
            "root": str(catalog.root),
            "work": str(work),
            "build": str(build),
            "python": sys.executable,
            "cc": os.environ.get("CC", "cc"),
        }
        build_config = spec.get("build")
        result = LabResult(lab_id=lab_id, build_passed=True)
        if build_config:
            argv = _expand(build_config["argv"], values)
            try:
                completed = _run(
                    argv,
                    cwd=work,
                    timeout=float(build_config.get("timeout", 20)),
                    sandbox_home=build,
                )
            except (subprocess.TimeoutExpired, OSError) as exc:
                result.build_passed = False
                result.build_output = f"{type(exc).__name__}: {exc}"
                return result
            result.build_output = completed.stdout
            result.build_passed = completed.returncode == int(
                build_config.get("expected_exit", 0)
            )
            if not result.build_passed:
                return result

        for index, case in enumerate(spec.get("tests", []), start=1):
            name = case.get("name", f"case-{index}")
            argv = _expand(case["argv"], values)
            try:
                completed = _run(
                    argv,
                    cwd=work,
                    timeout=float(case.get("timeout", 3)),
                    stdin=case.get("stdin", ""),
                    sandbox_home=build,
                )
            except (subprocess.TimeoutExpired, OSError) as exc:
                result.cases.append(
                    CaseResult(name=name, passed=False, detail=f"{type(exc).__name__}: {exc}")
                )
                continue
            expected_exit = int(case.get("expected_exit", 0))
            expected = _normal(case.get("expected_stdout", ""))
            actual = _normal(completed.stdout)
            mode = case.get("stdout_mode", "exact")
            output_ok = (
                actual == expected
                if mode == "exact"
                else expected in actual
                if mode == "contains"
                else False
            )
            passed = completed.returncode == expected_exit and output_ok
            detail = ""
            if not passed:
                detail = (
                    f"exit: expected {expected_exit}, got {completed.returncode}\n"
                    f"stdout ({mode}): expected {expected!r}, got {actual!r}"
                )
            result.cases.append(CaseResult(name=name, passed=passed, detail=detail))
        return result


def start_lab(
    catalog: Catalog,
    lab_id: str,
    destination: Path,
    force: bool = False,
) -> Path:
    lab_root = catalog.root / "labs" / lab_id
    spec = validate_lab_spec(catalog.lab_spec(lab_id), expected_id=lab_id)
    starter = lab_root / "starter"
    if not starter.is_dir():
        raise CourseError(f"Lab {lab_id} has no starter directory")
    native_tests = lab_root / "tests"
    native_support = catalog.root / "labs" / "test_support.h"
    native_make = catalog.root / "labs" / "c-test.mk"
    for asset in (native_tests / "test.c", native_support, native_make):
        if not asset.is_file():
            raise CourseError(
                f"Lab {lab_id} is missing native test asset "
                f"{asset.relative_to(catalog.root)}"
            )
    destination = destination.expanduser().resolve()
    if destination.exists():
        if not force:
            raise CourseError(
                f"Workspace already exists: {destination} (use --force to replace it)"
            )
        if not destination.is_dir():
            raise CourseError(
                f"Refusing to replace non-directory workspace: {destination}"
            )
        marker = destination / ".ftt-workspace.json"
        try:
            marker_data = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CourseError(
                f"Refusing to replace unrecognized directory: {destination}"
            ) from exc
        if (
            marker.is_symlink()
            or not isinstance(marker_data, dict)
            or marker_data.get("schema_version") != 1
            or marker_data.get("lab_id") != lab_id
            or marker_data.get("module") != spec["module"]
        ):
            raise CourseError(
                f"Refusing to replace workspace with an invalid marker: {destination}"
            )
        try:
            shutil.rmtree(destination)
        except OSError as exc:
            raise CourseError(f"Could not replace workspace: {destination}: {exc}") from exc
    shutil.copytree(starter, destination)
    shutil.copytree(native_tests, destination / "tests")
    shutil.copy2(native_support, destination / "test_support.h")
    shutil.copy2(native_make, destination / ".c-test.mk")
    (destination / "Makefile").write_text(
        "SOURCE ?= main.c\n"
        "TEST_SUPPORT_DIR ?= .\n"
        "include .c-test.mk\n",
        encoding="utf-8",
    )
    (destination / ".ftt-workspace.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "lab_id": lab_id,
                "module": spec["module"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    lab_readme = lab_root / "README.md"
    if lab_readme.is_file():
        shutil.copy2(lab_readme, destination / "LAB.md")
    module = catalog.module(spec["module"])
    page_name = Path(module["path"]).stem
    (destination / "WORKBOOK.md").write_text(
        f"# Workbook — {spec['title']}\n\n"
        f"Module: [[{page_name}]] (`{module['id']}`)  \n"
        f"Checker: `{lab_id}`\n\n"
        "## Prediction before running\n\n"
        "Write the expected state/output and the invariant that supports it.\n\n"
        "## Hand trace\n\n"
        "| step | input/state | operation | output/next state |\n"
        "|---:|---|---|---|\n"
        "| 0 | | | |\n\n"
        "## Experiments\n\n"
        "Record commands, observed output, and what each observation rules out.\n\n"
        "## Debugging record\n\n"
        "- Smallest failing case:\n"
        "- First wrong state:\n"
        "- Root cause:\n"
        "- Regression test:\n\n"
        "## Exit explanation\n\n"
        "Explain one invariant and one boundary case in your own words.\n",
        encoding="utf-8",
    )
    return destination

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from ftt.model import Catalog, CourseError
from ftt.runner import MAX_OUTPUT_BYTES, _run, run_lab, start_lab, validate_lab_spec


ROOT = Path(__file__).resolve().parents[1]


class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = Catalog.load(ROOT)

    def test_every_reference_solution_passes(self) -> None:
        for module in self.catalog.modules:
            lab_id = module.get("lab")
            if not lab_id:
                continue
            with self.subTest(lab=lab_id):
                result = run_lab(
                    self.catalog,
                    lab_id,
                    ROOT / "labs" / lab_id / "solution",
                )
                self.assertTrue(result.passed, result.build_output or result.cases)

    def test_every_starter_builds_but_fails_a_behavioral_case(self) -> None:
        for module in self.catalog.modules:
            lab_id = module.get("lab")
            if not lab_id:
                continue
            with self.subTest(lab=lab_id):
                result = run_lab(
                    self.catalog,
                    lab_id,
                    ROOT / "labs" / lab_id / "starter",
                )
                self.assertTrue(result.build_passed, result.build_output)
                self.assertTrue(result.cases, "a lab must exercise runtime behavior")
                self.assertTrue(
                    any(not case.passed for case in result.cases),
                    "the starter unexpectedly satisfies the complete lab contract",
                )

    def test_every_lab_uses_the_strict_c17_compile_contract(self) -> None:
        required_flags = {
            "-std=c17",
            "-O2",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wpedantic",
            "-Wconversion",
            "-Wsign-conversion",
            "-Wshadow",
        }
        for module in self.catalog.modules:
            lab_id = module.get("lab")
            if not lab_id:
                continue
            with self.subTest(lab=lab_id):
                spec = self.catalog.lab_spec(lab_id)
                argv = spec["build"]["argv"]
                self.assertEqual(argv[0], "{cc}")
                self.assertIn("{work}/main.c", argv)
                self.assertTrue(required_flags.issubset(argv), argv)
                self.assertGreaterEqual(len(spec["tests"]), 8)
                names = [case["name"] for case in spec["tests"]]
                self.assertEqual(len(names), len(set(names)))
                self.assertTrue(any(case.get("expected_exit", 0) == 0 for case in spec["tests"]))
                self.assertTrue(any(case.get("expected_exit", 0) != 0 for case in spec["tests"]))

    def test_assembler_cases_cover_every_cpu_opcode_contract(self) -> None:
        spec = self.catalog.lab_spec("lab-03-assembler")
        operations = {
            case["argv"][2]
            for case in spec["tests"]
            if len(case["argv"]) >= 3 and case["argv"][1] == "asm"
        }
        self.assertEqual(
            operations,
            {"halt", "ldi", "add", "xor", "load", "store", "jmp", "jz"},
        )

    def test_jtag_cases_cover_both_outgoing_edges_of_all_states(self) -> None:
        spec = self.catalog.lab_spec("lab-07-jtag")
        exhaustive = next(
            case for case in spec["tests"] if case["name"] == "all-32-tap-transitions"
        )
        lines = exhaustive["expected_stdout"].splitlines()
        state = lines[0].split("state=", 1)[1]
        covered: set[tuple[str, int]] = set()
        for line in lines[1:]:
            if not line.startswith("clock="):
                continue
            fields = line.split()
            tms = int(fields[1].split("=", 1)[1])
            covered.add((state, tms))
            state = fields[2].split("=", 1)[1]
        self.assertEqual(len(covered), 32)
        states = {state_name for state_name, _ in covered}
        self.assertEqual(len(states), 16)
        for state_name in states:
            self.assertEqual(
                {tms for source, tms in covered if source == state_name},
                {0, 1},
            )

    def test_lab_spec_fails_closed_on_empty_or_malformed_tests(self) -> None:
        base = {
            "schema_version": 1,
            "id": "lab-demo",
            "module": "00.01",
            "title": "Demo",
        }
        with self.assertRaises(CourseError):
            validate_lab_spec({**base, "tests": []}, expected_id="lab-demo")
        with self.assertRaises(CourseError):
            validate_lab_spec(
                {
                    **base,
                    "tests": [
                        {"name": f"case-{index}", "argv": ["{unknown}"]}
                        for index in range(3)
                    ],
                },
                expected_id="lab-demo",
            )

    def test_start_marks_workspace_and_force_is_scoped(self) -> None:
        lab_id = next(m["lab"] for m in self.catalog.modules if m.get("lab"))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "work"
            start_lab(self.catalog, lab_id, destination)
            marker = json.loads(
                (destination / ".ftt-workspace.json").read_text(encoding="utf-8")
            )
            self.assertEqual(marker["lab_id"], lab_id)
            self.assertTrue((destination / "tests" / "test.c").is_file())
            self.assertTrue((destination / "test_support.h").is_file())
            self.assertTrue((destination / ".c-test.mk").is_file())
            self.assertIn("SOURCE ?= main.c", (destination / "Makefile").read_text())
            start_lab(self.catalog, lab_id, destination, force=True)

            unowned = Path(temporary) / "unowned"
            unowned.mkdir()
            (unowned / "important.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(CourseError):
                start_lab(self.catalog, lab_id, unowned, force=True)
            self.assertTrue((unowned / "important.txt").is_file())

            existing_file = Path(temporary) / "existing-file"
            existing_file.write_text("keep", encoding="utf-8")
            with self.assertRaises(CourseError):
                start_lab(self.catalog, lab_id, existing_file, force=True)
            self.assertEqual(existing_file.read_text(encoding="utf-8"), "keep")

    def test_runaway_program_is_timed_out(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            with self.assertRaises(subprocess.TimeoutExpired):
                _run(
                    [sys.executable, "-c", "while True: pass"],
                    cwd=directory,
                    timeout=0.1,
                    sandbox_home=directory,
                )

    def test_started_workspace_runs_its_own_native_c_suite(self) -> None:
        lab_id = "lab-00-bytes"
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "workspace"
            start_lab(self.catalog, lab_id, destination)
            starter = subprocess.run(
                ["make", "--no-print-directory", "test"],
                cwd=destination,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertNotEqual(starter.returncode, 0, starter.stdout)
            self.assertIn("not ok", starter.stdout)

            shutil.copy2(
                ROOT / "labs" / lab_id / "solution" / "main.c",
                destination / "main.c",
            )
            completed = subprocess.run(
                ["make", "--no-print-directory", "test"],
                cwd=destination,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("8/8 native C cases passed", completed.stdout)

    def test_output_is_binary_safe_and_memory_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            binary = _run(
                [sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'\\xff')"],
                cwd=directory,
                timeout=2,
                sandbox_home=directory,
            )
            self.assertEqual(binary.stdout, "\ufffd")
            noisy = _run(
                [
                    sys.executable,
                    "-c",
                    f"import sys; sys.stdout.write('x' * {MAX_OUTPUT_BYTES + 4096})",
                ],
                cwd=directory,
                timeout=2,
                sandbox_home=directory,
            )
            self.assertIn("[output truncated]", noisy.stdout)
            self.assertLessEqual(len(noisy.stdout), MAX_OUTPUT_BYTES + 32)


if __name__ == "__main__":
    unittest.main()

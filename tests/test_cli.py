from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ftt.cli import main
from ftt.model import Catalog


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *argv: str) -> tuple[int, str, str]:
        stdout, stderr = StringIO(), StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(["--root", str(ROOT), *argv])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_read_only_commands(self) -> None:
        code, output, _ = self.run_cli("list", "--section", "03")
        self.assertEqual(code, 0)
        self.assertIn("Assembler", output)
        code, output, _ = self.run_cli("show", "03.01", "--path")
        self.assertEqual(code, 0)
        self.assertIn("03.01", output)
        code, output, _ = self.run_cli("validate")
        self.assertEqual(code, 0, output)

    def test_exam_can_be_graded(self) -> None:
        catalog = Catalog.load(ROOT)
        exam = catalog.exams[0]
        bank = json.loads((ROOT / exam["bank"]).read_text(encoding="utf-8"))
        answers = ",".join(question["answer"] for question in bank["questions"])
        code, output, _ = self.run_cli("exam", exam["id"], "--answers", answers)
        self.assertEqual(code, 0)
        self.assertIn("100%", output)

    def test_start_check_and_progress_use_isolated_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary) / "state"
            work = Path(temporary) / "work"
            environment = {"FTT_STATE_DIR": str(state), "FTT_WORK_DIR": str(work)}
            with patch.dict(os.environ, environment):
                code, output, _ = self.run_cli("start", "00.04")
                self.assertEqual(code, 0, output)
                code, output, _ = self.run_cli("check", "00.04")
                self.assertEqual(code, 1, output)
                code, output, _ = self.run_cli("check", "00.04", "--solution")
                self.assertEqual(code, 0, output)
                code, output, _ = self.run_cli("progress", "--json")
                self.assertEqual(code, 0)
                self.assertEqual(json.loads(output)["completed"], 0)


if __name__ == "__main__":
    unittest.main()

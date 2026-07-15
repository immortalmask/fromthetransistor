from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class NotebookSuiteTests(unittest.TestCase):
    def test_notebooks_execute_cumulatively_without_stored_outputs(self) -> None:
        completed = subprocess.run(
            [sys.executable, "tools/check_notebooks.py"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertIn("PASS: 5 notebooks executed cumulatively", completed.stdout)


if __name__ == "__main__":
    unittest.main()

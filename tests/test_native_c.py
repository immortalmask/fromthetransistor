from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from ftt.model import Catalog


ROOT = Path(__file__).resolve().parents[1]
CASE_NAME = re.compile(r'CTEST_CASE\(\s*"([^"]+)"')


class NativeCTestSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = Catalog.load(ROOT)
        cls.lab_ids = [
            module["lab"] for module in cls.catalog.modules if module.get("lab")
        ]

    def test_every_json_case_has_a_colocated_native_c_case(self) -> None:
        self.assertEqual(len(self.lab_ids), 12)
        for lab_id in self.lab_ids:
            with self.subTest(lab=lab_id):
                lab_root = ROOT / "labs" / lab_id
                source = lab_root / "tests" / "test.c"
                self.assertTrue(source.is_file(), source)
                self.assertTrue((lab_root / "Makefile").is_file())
                text = source.read_text(encoding="utf-8")
                native_names = CASE_NAME.findall(text)
                json_names = [
                    case["name"] for case in self.catalog.lab_spec(lab_id)["tests"]
                ]
                self.assertEqual(native_names, json_names)
                self.assertNotIn("solution/main.c", text)
                self.assertNotIn("starter/main.c", text)

    def test_every_starter_compiles_but_fails_the_native_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ftt-native-starters-") as temporary:
            build_root = Path(temporary)
            for lab_id in self.lab_ids:
                lab_root = ROOT / "labs" / lab_id
                with self.subTest(lab=lab_id):
                    completed = subprocess.run(
                        [
                            "make",
                            "--no-print-directory",
                            "-C",
                            str(lab_root),
                            "test",
                            f"SOURCE={lab_root / 'starter' / 'main.c'}",
                            f"BUILD_DIR={build_root / lab_id}",
                        ],
                        cwd=ROOT,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        check=False,
                    )
                    self.assertNotEqual(completed.returncode, 0, completed.stdout)
                    self.assertIn("not ok", completed.stdout)


if __name__ == "__main__":
    unittest.main()

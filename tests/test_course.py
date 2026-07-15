import importlib.util
from pathlib import Path
import json
import subprocess
import sys
import unittest

from ftt.model import Catalog
from ftt.validation import validate


ROOT = Path(__file__).resolve().parents[1]


class AuthoredCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = Catalog.load(ROOT)

    def test_full_source_outline_is_mapped(self) -> None:
        self.assertEqual(len(self.catalog.sections), 8)
        self.assertEqual(len(self.catalog.modules), 32)
        self.assertEqual(sum(bool(m.get("source_ref")) for m in self.catalog.modules), 24)

    def test_course_validates(self) -> None:
        self.assertEqual(validate(self.catalog), [])

    def test_practical_core_is_present(self) -> None:
        labs = [module["lab"] for module in self.catalog.modules if module.get("lab")]
        self.assertEqual(len(labs), 12)
        self.assertEqual(len(set(labs)), 12)
        self.assertEqual(len(self.catalog.exams), 7)

    def test_every_module_has_curated_external_sources(self) -> None:
        references = json.loads(
            (ROOT / "course" / "references.json").read_text(encoding="utf-8")
        )
        expected = {module["id"] for module in self.catalog.modules} | {"capstone"}
        self.assertEqual(set(references["items"]), expected)
        for item_id, entries in references["items"].items():
            with self.subTest(item=item_id):
                self.assertGreaterEqual(len(entries), 2)
                self.assertLessEqual(len(entries), 4)
                self.assertTrue(any(entry["tier"] == "start" for entry in entries))
                self.assertTrue(all(entry["url"].startswith("https://") for entry in entries))

    def test_external_sources_are_synchronized(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/sync_references.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"{result.stdout}{result.stderr}",
        )


class ReferenceRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = ROOT / "tools" / "sync_references.py"
        spec = importlib.util.spec_from_file_location("ftt_sync_references", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"could not load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.renderer = module

    def test_replace_block_rejects_unpaired_marker(self) -> None:
        text = "\n".join(
            [
                "## External sources",
                "",
                self.renderer.START_MARKER,
                "",
                "## Exit criteria",
                "",
            ]
        )
        with self.assertRaises(self.renderer.ReferenceError):
            self.renderer.replace_block(
                text,
                "replacement",
                "## Exit criteria",
                Path("example.md"),
            )

    def test_page_map_rejects_path_outside_repository(self) -> None:
        catalog = {"modules": [{"id": "escape", "path": "../escape.md"}]}
        with self.assertRaises(self.renderer.ReferenceError):
            self.renderer.page_map(catalog)

    def test_validate_data_rejects_impossible_and_future_dates(self) -> None:
        entry = {
            "title": "Example",
            "url": "https://example.com/reference",
            "kind": "manual",
            "tier": "start",
            "use": "Check the example contract.",
        }
        catalog = {"modules": []}
        for verified_on in ("2026-99-99", "2999-01-01"):
            references = {
                "schema_version": 1,
                "verified_on": verified_on,
                "items": {
                    "capstone": [
                        entry,
                        {**entry, "url": "https://example.com/two"},
                    ]
                },
            }
            with self.subTest(verified_on=verified_on):
                with self.assertRaises(self.renderer.ReferenceError):
                    self.renderer.validate_data(catalog, references)


if __name__ == "__main__":
    unittest.main()

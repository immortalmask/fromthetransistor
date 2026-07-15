from pathlib import Path
import tempfile
import unittest

from ftt.model import Catalog, CourseError, find_root, parse_frontmatter


ROOT = Path(__file__).resolve().parents[1]


class FrontmatterTests(unittest.TestCase):
    def test_parses_json_compatible_values_and_preserves_body(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "page.md"
            path.write_text(
                '---\nid: "00.01"\ntags: ["c", "tools"]\noptional: false\n---\n# Body\n',
                encoding="utf-8",
            )
            metadata, body = parse_frontmatter(path)
        self.assertEqual(metadata["id"], "00.01")
        self.assertEqual(metadata["tags"], ["c", "tools"])
        self.assertFalse(metadata["optional"])
        self.assertEqual(body, "# Body\n")

    def test_rejects_unclosed_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "page.md"
            path.write_text("---\nid: x\n", encoding="utf-8")
            with self.assertRaises(CourseError):
                parse_frontmatter(path)

    def test_rejects_duplicate_frontmatter_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "page.md"
            path.write_text("---\nid: first\nid: second\n---\n", encoding="utf-8")
            with self.assertRaises(CourseError):
                parse_frontmatter(path)

    def test_finds_checkout_root(self) -> None:
        self.assertEqual(find_root(ROOT / "src"), ROOT)

    def test_catalog_rejects_path_escape(self) -> None:
        catalog = Catalog.load(ROOT)
        with self.assertRaises(CourseError):
            catalog.safe_path("../outside")


if __name__ == "__main__":
    unittest.main()

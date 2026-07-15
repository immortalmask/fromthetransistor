import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ftt.model import CourseError
from ftt.progress import ProgressStore


class ProgressTests(unittest.TestCase):
    def test_round_trip_and_unmark(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary) / "state"
            with patch.dict(os.environ, {"FTT_STATE_DIR": str(state)}):
                store = ProgressStore(Path(temporary))
                store.mark_module("00.01", "compiled hello", "manual")
                store.record_lab("lab-demo", True, 3)
                store.mark_challenge("H00.01", "evidence.json", "a" * 64)
                data = store.read()
                self.assertEqual(data["modules"]["00.01"]["evidence"], "compiled hello")
                self.assertIn("passed_at", data["labs"]["lab-demo"])
                self.assertEqual(
                    data["challenges"]["H00.01"]["evidence"], "evidence.json"
                )
                store.unmark_module("00.01")
                self.assertNotIn("00.01", store.read()["modules"])
                json.loads(store.path.read_text(encoding="utf-8"))

    def test_corrupt_progress_is_reported_not_discarded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary) / "state"
            state.mkdir()
            (state / "progress.json").write_text("not json", encoding="utf-8")
            with patch.dict(os.environ, {"FTT_STATE_DIR": str(state)}):
                with self.assertRaises(CourseError):
                    ProgressStore(Path(temporary)).read()


if __name__ == "__main__":
    unittest.main()

from contextlib import redirect_stderr, redirect_stdout
import copy
import hashlib
import importlib.util
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from ftt.challenges import (
    ChallengeCatalog,
    check_evidence,
    start_challenge,
    validate_challenges,
)
from ftt.cli import main
from ftt.model import Catalog, CourseError
from ftt.progress import ProgressStore


ROOT = Path(__file__).resolve().parents[1]


class ChallengeCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = Catalog.load(ROOT)
        cls.catalog = ChallengeCatalog.load(ROOT)

    def test_track_is_large_cumulative_and_valid(self) -> None:
        self.assertEqual([pack["id"] for pack in self.catalog.packs], [f"{n:02d}" for n in range(8)])
        self.assertEqual(len(self.catalog.challenges), 64)
        self.assertTrue(all(len(pack["challenges"]) == 8 for pack in self.catalog.packs))
        self.assertEqual(validate_challenges(self.course, self.catalog), [])

    def test_malformed_catalog_top_level_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "course").mkdir()
            (root / "course" / "challenges.json").write_text("[]\n", encoding="utf-8")
            with self.assertRaises(CourseError):
                ChallengeCatalog.load(root)

    def test_every_stage_has_multiple_lanes_and_a_boss(self) -> None:
        for pack in self.catalog.packs:
            with self.subTest(stage=pack["id"]):
                lanes = {challenge["lane"] for challenge in pack["challenges"]}
                self.assertGreaterEqual(len(lanes), 4)
                self.assertEqual(sum(challenge["lane"] == "boss" for challenge in pack["challenges"]), 1)
                self.assertEqual(
                    {stars: sum(c["stars"] == stars for c in pack["challenges"]) for stars in (1, 2, 3)},
                    {1: 2, 2: 5, 3: 1},
                )
                self.assertEqual(pack["challenges"][-1]["stars"], 3)

    def test_rendered_pages_are_synchronized(self) -> None:
        completed = subprocess.run(
            [sys.executable, "tools/sync_challenges.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_renderer_rejects_unsafe_or_duplicate_destinations(self) -> None:
        path = ROOT / "tools" / "sync_challenges.py"
        spec = importlib.util.spec_from_file_location("ftt_sync_challenges", path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderer)

        unsafe_raw = copy.deepcopy(self.catalog.raw)
        unsafe_raw["packs"][0]["path"] = "src/ftt/cli.py"
        with self.assertRaises(CourseError):
            renderer.expected_pages(ChallengeCatalog(ROOT, unsafe_raw))

        duplicate_raw = copy.deepcopy(self.catalog.raw)
        duplicate_raw["packs"][1]["path"] = duplicate_raw["packs"][0]["path"]
        with self.assertRaises(CourseError):
            renderer.expected_pages(ChallengeCatalog(ROOT, duplicate_raw))


class ChallengeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = ChallengeCatalog.load(ROOT)
        cls.challenge = cls.catalog.challenges[0]

    def make_packet(self, work: Path) -> dict[str, object]:
        report = work / "REPORT.md"
        report.write_text("A sufficiently detailed engineering report.\n", encoding="utf-8")
        trace = work / "trace.jsonl"
        trace.write_text('{"event":"accepted"}\n', encoding="utf-8")

        def digest(path: Path) -> str:
            return hashlib.sha256(path.read_bytes()).hexdigest()

        return {
            "schema_version": 1,
            "challenge_id": self.challenge["id"],
            "claim": {
                "invariant": "Every accepted record round-trips to exactly the same canonical bytes.",
                "first_divergence": "The deliberately corrupt record first diverges at checksum byte seventeen.",
                "limitations": "This demonstration checks the packet protocol, not the open design rubric itself.",
            },
            "artifacts": [
                {"path": "REPORT.md", "sha256": digest(report)},
                {"path": "trace.jsonl", "sha256": digest(trace)},
            ],
            "acceptance": {
                criterion["id"]: ["REPORT.md", "trace.jsonl"]
                for criterion in self.challenge["acceptance"]
            },
            "replay": [
                {
                    "name": "canonical record",
                    "kind": "positive",
                    "argv": ["{python}", "-c", "print('roundtrip ok')"],
                    "expected_exit": 0,
                    "output_contains": ["roundtrip ok"],
                    "timeout_seconds": 5,
                },
                {
                    "name": "corrupt record is rejected",
                    "kind": "negative",
                    "argv": ["{python}", "-c", "print('checksum rejected')"],
                    "expected_exit": 0,
                    "output_contains": ["checksum rejected"],
                    "timeout_seconds": 5,
                },
            ],
        }

    @staticmethod
    def write_packet(work: Path, packet: object) -> None:
        (work / "evidence.json").write_text(
            json.dumps(packet, indent=2) + "\n", encoding="utf-8"
        )

    def test_fresh_workspace_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertFalse(result.passed)
            self.assertTrue(any("claim.invariant" in error for error in result.errors))
            self.assertEqual(result.replays, ())

    def test_force_only_overwrites_matching_marked_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            arbitrary = Path(temporary) / "arbitrary"
            arbitrary.mkdir()
            (arbitrary / "valuable.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(CourseError):
                start_challenge(
                    self.catalog, self.challenge["id"], arbitrary, force=True
                )
            self.assertEqual(
                (arbitrary / "valuable.txt").read_text(encoding="utf-8"), "keep"
            )

            marked = Path(temporary) / "marked"
            start_challenge(self.catalog, self.challenge["id"], marked)
            start_challenge(self.catalog, self.challenge["id"], marked, force=True)

    def test_complete_packet_hashes_and_replays(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            packet = self.make_packet(work)
            self.write_packet(work, packet)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertTrue(result.passed, result)
            self.assertEqual(len(result.replays), 2)

    def test_artifacts_cannot_escape_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            packet = json.loads((work / "evidence.json").read_text(encoding="utf-8"))
            packet["artifacts"] = [{"path": "../outside", "sha256": "0" * 64}]
            (work / "evidence.json").write_text(json.dumps(packet), encoding="utf-8")
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertTrue(any("escapes workspace" in error for error in result.errors))

    def test_structural_failure_never_executes_replay(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            packet = self.make_packet(work)
            packet["artifacts"][0]["sha256"] = "0" * 64
            packet["replay"][0]["argv"] = [
                "{python}",
                "-c",
                "from pathlib import Path; Path('SHOULD_NOT_EXIST').touch()",
            ]
            packet["replay"][0]["output_contains"] = []
            self.write_packet(work, packet)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertFalse(result.passed)
            self.assertEqual(result.replays, ())
            self.assertFalse((work / "SHOULD_NOT_EXIST").exists())

    def test_duplicate_artifact_aliases_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            packet = self.make_packet(work)
            packet["artifacts"][1] = {
                "path": "./REPORT.md",
                "sha256": packet["artifacts"][0]["sha256"],
            }
            self.write_packet(work, packet)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertTrue(any("aliases" in error for error in result.errors))

    def test_hard_linked_artifacts_are_not_two_independent_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            packet = self.make_packet(work)
            (work / "trace.jsonl").unlink()
            os.link(work / "REPORT.md", work / "trace.jsonl")
            packet["artifacts"][1]["sha256"] = packet["artifacts"][0]["sha256"]
            self.write_packet(work, packet)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertTrue(any("hard-links" in error for error in result.errors))

    def test_replay_cannot_mutate_hashed_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            packet = self.make_packet(work)
            packet["replay"][1]["argv"] = [
                "{python}",
                "-c",
                "from pathlib import Path; Path('REPORT.md').write_text('changed')",
            ]
            packet["replay"][1]["output_contains"] = []
            self.write_packet(work, packet)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertFalse(result.passed)
            self.assertTrue(any("changed during replay" in error for error in result.errors))

    def test_malformed_packet_values_fail_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            self.write_packet(work, [])
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertIn("JSON object", result.errors[0])
            packet = self.make_packet(work)
            first = next(iter(packet["acceptance"]))
            packet["acceptance"][first] = [{}]
            self.write_packet(work, packet)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertTrue(any("references must be strings" in error for error in result.errors))

    def test_invalid_utf8_replay_output_is_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            packet = self.make_packet(work)
            packet["replay"][0]["argv"] = [
                "{python}",
                "-c",
                "import sys; sys.stdout.buffer.write(b'\\xffroundtrip ok\\n')",
            ]
            self.write_packet(work, packet)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertTrue(result.passed, result)

    def test_truncated_replay_output_cannot_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "challenge"
            start_challenge(self.catalog, self.challenge["id"], work)
            packet = self.make_packet(work)
            packet["replay"][0]["argv"] = [
                "{python}",
                "-c",
                "print('x' * (2 * 1024 * 1024))",
            ]
            packet["replay"][0]["output_contains"] = []
            self.write_packet(work, packet)
            result = check_evidence(self.catalog, self.challenge["id"], work)
            self.assertFalse(result.passed)
            self.assertTrue(any("output exceeded" in replay.detail for replay in result.replays))


class ChallengeCliTests(unittest.TestCase):
    def run_cli(self, *argv: str) -> tuple[int, str, str]:
        stdout, stderr = StringIO(), StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(["--root", str(ROOT), *argv])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_list_and_show(self) -> None:
        code, output, error = self.run_cli("challenge", "list", "--stage", "03")
        self.assertEqual(code, 0, error)
        self.assertIn("H03.01", output)
        self.assertIn("*   ISA Archaeology", output)
        self.assertIn("Boss", output)
        code, output, error = self.run_cli("challenge", "show", "H03.01")
        self.assertEqual(code, 0, error)
        self.assertIn("Adversarial campaign", output)

    def test_started_packet_fails_until_evidence_is_supplied(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = str(Path(temporary) / "work")
            code, output, error = self.run_cli(
                "challenge", "start", "H00.01", "--work", work
            )
            self.assertEqual(code, 0, output + error)
            self.assertIn(f"--work {work}", output)
            code, output, error = self.run_cli(
                "challenge", "check", "H00.01", "--work", work, "--no-record"
            )
            self.assertEqual(code, 1, output + error)
            self.assertIn("result FAIL", output)

    def test_changed_recorded_packet_is_marked_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary) / "state"
            evidence = Path(temporary) / "evidence.json"
            evidence.write_text("original\n", encoding="utf-8")
            digest = hashlib.sha256(evidence.read_bytes()).hexdigest()
            with patch.dict(os.environ, {"FTT_STATE_DIR": str(state)}):
                ProgressStore(ROOT).mark_challenge(
                    "H00.01", str(evidence), digest
                )
                code, output, error = self.run_cli(
                    "challenge", "list", "--stage", "00"
                )
                self.assertEqual(code, 0, error)
                self.assertIn("[x] H00.01", output)
                evidence.write_text("changed\n", encoding="utf-8")
                code, output, error = self.run_cli(
                    "challenge", "list", "--stage", "00"
                )
                self.assertEqual(code, 0, error)
                self.assertIn("[!] H00.01", output)


if __name__ == "__main__":
    unittest.main()

"""Small, local, auditable progress store."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from .model import CourseError


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class ProgressStore:
    def __init__(self, root: Path):
        state_dir = Path(os.environ.get("FTT_STATE_DIR", root / ".ftt"))
        self.path = state_dir.expanduser().resolve() / "progress.json"

    def read(self) -> dict[str, Any]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {"schema_version": 1, "modules": {}, "labs": {}, "challenges": {}}
        except json.JSONDecodeError as exc:
            raise CourseError(f"Progress file is not valid JSON: {self.path}: {exc}") from exc
        if data.get("schema_version") != 1:
            raise CourseError(f"Unsupported progress schema in {self.path}")
        data.setdefault("modules", {})
        data.setdefault("labs", {})
        data.setdefault("challenges", {})
        return data

    def write(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
        fd, temporary = tempfile.mkstemp(
            prefix="progress-", suffix=".json", dir=self.path.parent
        )
        temp_path = Path(temporary)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            temp_path.replace(self.path)
        finally:
            temp_path.unlink(missing_ok=True)

    def mark_module(self, module_id: str, evidence: str, source: str) -> None:
        data = self.read()
        data["modules"][module_id] = {
            "completed_at": now_iso(),
            "evidence": evidence,
            "source": source,
        }
        self.write(data)

    def record_lab(self, lab_id: str, passed: bool, tests: int) -> None:
        data = self.read()
        entry = data["labs"].setdefault(lab_id, {"attempts": []})
        entry["attempts"].append(
            {"at": now_iso(), "passed": passed, "tests": tests}
        )
        entry["attempts"] = entry["attempts"][-50:]
        if passed:
            entry["passed_at"] = now_iso()
        self.write(data)

    def unmark_module(self, module_id: str) -> None:
        data = self.read()
        data["modules"].pop(module_id, None)
        self.write(data)

    def mark_challenge(
        self,
        challenge_id: str,
        evidence: str,
        evidence_digest: str,
        waived_prerequisites: list[str] | None = None,
    ) -> None:
        data = self.read()
        data["challenges"][challenge_id] = {
            "completed_at": now_iso(),
            "evidence": evidence,
            "evidence_digest": evidence_digest,
            "source": "challenge-replay",
            "waived_prerequisites": waived_prerequisites or [],
        }
        self.write(data)

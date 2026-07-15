"""Advanced challenge catalog, workspaces, and replayable evidence packets."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from .model import Catalog, CourseError
from .runner import OUTPUT_TRUNCATED_MARKER, run_argv_limited


CHALLENGE_ID = re.compile(r"^H(?P<stage>0[0-7])\.(?P<number>0[1-9]|[1-9][0-9])$")
LANES = {"archaeology", "construction", "adversary", "integration", "boss"}
DIFFICULTIES = {"hard", "very hard", "brutal"}
REPLAY_KINDS = {"positive", "negative"}
MAX_REPLAY_TIMEOUT = 120
STAR_TIER_NAMES = {
    1: "focused",
    2: "cumulative",
    3: "boss-scale",
}


def _markdown_stars(count: int) -> str:
    return "\\*" * count


@dataclass(frozen=True)
class ReplayResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass(frozen=True)
class EvidenceResult:
    errors: tuple[str, ...]
    replays: tuple[ReplayResult, ...]

    @property
    def passed(self) -> bool:
        return not self.errors and all(replay.passed for replay in self.replays)


@dataclass(frozen=True)
class ChallengeCatalog:
    root: Path
    raw: dict[str, Any]

    @classmethod
    def load(cls, root: Path) -> "ChallengeCatalog":
        path = root / "course" / "challenges.json"
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise CourseError(f"Missing challenge catalog: {path}") from exc
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise CourseError(f"Invalid challenge catalog {path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise CourseError("Challenge catalog must be a JSON object")
        if raw.get("schema_version") != 1:
            raise CourseError("Unsupported challenge schema_version (expected 1)")
        if not isinstance(raw.get("track"), dict):
            raise CourseError("Challenge catalog track must be an object")
        if not isinstance(raw.get("packs"), list):
            raise CourseError("Challenge catalog packs must be a list")
        for index, pack in enumerate(raw["packs"], start=1):
            if not isinstance(pack, dict):
                raise CourseError(f"Challenge pack {index} must be an object")
            if not isinstance(pack.get("challenges"), list):
                raise CourseError(f"Challenge pack {index} challenges must be a list")
            if any(not isinstance(item, dict) for item in pack["challenges"]):
                raise CourseError(f"Challenge pack {index} contains a non-object challenge")
        return cls(root=root, raw=raw)

    @property
    def track(self) -> dict[str, Any]:
        return self.raw.get("track", {})

    @property
    def packs(self) -> list[dict[str, Any]]:
        return self.raw["packs"]

    @property
    def challenges(self) -> list[dict[str, Any]]:
        return [challenge for pack in self.packs for challenge in pack.get("challenges", [])]

    def pack(self, stage: str) -> dict[str, Any]:
        for pack in self.packs:
            if pack.get("id") == stage:
                return pack
        for pack in self.packs:
            if pack.get("slug") == stage:
                return pack
        raise CourseError(f"Unknown challenge stage: {stage}")

    def challenge(self, challenge_id: str) -> dict[str, Any]:
        normalized = challenge_id.upper()
        for challenge in self.challenges:
            if challenge.get("id") == normalized:
                return challenge
        for challenge in self.challenges:
            if challenge.get("slug") == challenge_id:
                return challenge
        raise CourseError(f"Unknown challenge: {challenge_id}")

    def challenge_pack(self, challenge_id: str) -> dict[str, Any]:
        challenge = self.challenge(challenge_id)
        return self.pack(str(challenge["stage"]))

    def safe_path(self, relative: str | Path) -> Path:
        return Catalog.load(self.root).safe_path(relative)


def _duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def validate_challenges(course: Catalog, catalog: ChallengeCatalog) -> list[str]:
    """Validate depth, dependency, source, and evidence requirements."""

    errors: list[str] = []
    if not isinstance(catalog.track.get("description"), str) or len(
        catalog.track.get("description", "").strip()
    ) < 24:
        errors.append("challenge track needs a substantive description")
    packs = catalog.packs
    module_ids = {module["id"] for module in course.modules}
    pack_ids = [str(pack.get("id", "")) for pack in packs]
    pack_slugs = [str(pack.get("slug", "")) for pack in packs]
    if pack_ids != [f"{number:02d}" for number in range(8)]:
        errors.append("challenge packs must be ordered exactly 00 through 07")
    for duplicate in sorted(_duplicates(pack_ids)):
        errors.append(f"duplicate challenge pack: {duplicate}")
    for duplicate in sorted(_duplicates(pack_slugs)):
        errors.append(f"duplicate challenge pack slug: {duplicate}")
    for slug in pack_slugs:
        if not slug or slug in set(pack_ids):
            errors.append(f"invalid or colliding challenge pack slug: {slug!r}")

    all_challenges = catalog.challenges
    challenge_ids = [str(challenge.get("id", "")) for challenge in all_challenges]
    challenge_slugs = [str(challenge.get("slug", "")) for challenge in all_challenges]
    challenge_set = set(challenge_ids)
    for duplicate in sorted(_duplicates(challenge_ids)):
        errors.append(f"duplicate challenge id: {duplicate}")
    for duplicate in sorted(_duplicates(challenge_slugs)):
        errors.append(f"duplicate challenge slug: {duplicate}")
    for slug in challenge_slugs:
        if not slug or slug.upper() in set(challenge_ids):
            errors.append(f"invalid or colliding challenge slug: {slug!r}")
    if len(all_challenges) != 64:
        errors.append(f"advanced track needs exactly 64 challenges, found {len(all_challenges)}")

    known_sources: set[str] = set()
    page_paths: set[Path] = set()
    for pack in packs:
        stage = str(pack.get("id", ""))
        challenges = pack.get("challenges")
        if not isinstance(challenges, list) or len(challenges) != 8:
            errors.append(f"challenge pack {stage}: expected exactly 8 challenges")
            challenges = []
        expected_stage_ids = [f"H{stage}.{number:02d}" for number in range(1, 9)]
        actual_stage_ids = [
            str(challenge.get("id", ""))
            for challenge in challenges
            if isinstance(challenge, dict)
        ]
        if actual_stage_ids != expected_stage_ids:
            errors.append(
                f"challenge pack {stage}: ids must be ordered {expected_stage_ids[0]} through {expected_stage_ids[-1]}"
            )
        lanes = {
            challenge.get("lane")
            for challenge in challenges
            if isinstance(challenge, dict)
        }
        if len(lanes & LANES) < 4:
            errors.append(f"challenge pack {stage}: needs at least four distinct lanes")
        star_counts = {
            stars: sum(
                challenge.get("stars") == stars
                for challenge in challenges
                if isinstance(challenge, dict)
            )
            for stars in STAR_TIER_NAMES
        }
        if star_counts != {1: 2, 2: 5, 3: 1}:
            errors.append(
                f"challenge pack {stage}: expected star distribution 2 focused, 5 cumulative, 1 boss"
            )
        bosses = [
            challenge
            for challenge in challenges
            if isinstance(challenge, dict) and challenge.get("lane") == "boss"
        ]
        if len(bosses) != 1:
            errors.append(f"challenge pack {stage}: needs exactly one boss")
        elif bosses[0].get("id") != f"H{stage}.08":
            errors.append(f"challenge pack {stage}: boss must be H{stage}.08")
        elif len(
            [
                item
                for item in bosses[0].get("prerequisites", [])
                if isinstance(item, str) and item.startswith(f"H{stage}.")
            ]
        ) < 3:
            errors.append(f"challenge pack {stage}: boss needs three same-stage challenges")
        for field in ("title", "overview", "entry_gate", "stage_handoff"):
            if not isinstance(pack.get(field), str) or len(pack[field].strip()) < 12:
                errors.append(f"challenge pack {stage}: missing or shallow {field}")
        path_value = pack.get("path")
        if not isinstance(path_value, str):
            errors.append(f"challenge pack {stage}: missing page path")
        else:
            try:
                path = course.safe_path(path_value)
                challenge_root = (course.root / "vault" / "Challenges").resolve()
                if path.parent != challenge_root or path.suffix != ".md":
                    errors.append(
                        f"challenge pack {stage}: page must be a Markdown file directly in vault/Challenges"
                    )
                if path in page_paths:
                    errors.append(f"challenge pack {stage}: duplicate generated page {path_value}")
                page_paths.add(path)
                if not path.is_file():
                    errors.append(f"challenge pack {stage}: missing page {path_value}")
            except CourseError as exc:
                errors.append(f"challenge pack {stage}: {exc}")
        sources = pack.get("sources")
        if not isinstance(sources, list) or len(sources) < 3:
            errors.append(f"challenge pack {stage}: expected at least 3 primary sources")
            sources = []
        for index, source in enumerate(sources, start=1):
            if not isinstance(source, dict):
                errors.append(f"challenge pack {stage} source {index}: must be an object")
                continue
            for field in ("title", "url", "use"):
                if not isinstance(source.get(field), str) or not source[field].strip():
                    errors.append(f"challenge pack {stage} source {index}: missing {field}")
            url = source.get("url")
            if isinstance(url, str):
                if not url.startswith("https://"):
                    errors.append(f"challenge pack {stage} source {index}: URL must use HTTPS")
                if url in known_sources:
                    errors.append(f"challenge source URL reused across packs: {url}")
                known_sources.add(url)

        for challenge in challenges:
            challenge_id = str(challenge.get("id", "<missing>"))
            match = CHALLENGE_ID.fullmatch(challenge_id)
            if match is None:
                errors.append(f"invalid challenge id: {challenge_id}")
            elif match.group("stage") != stage:
                errors.append(f"{challenge_id}: id does not match stage {stage}")
            if challenge.get("stage") != stage:
                errors.append(f"{challenge_id}: stage field does not match pack {stage}")
            if not isinstance(challenge.get("title"), str) or len(
                challenge["title"].strip()
            ) < 4:
                errors.append(f"{challenge_id}: missing or shallow title")
            for field in ("brief", "artifact", "handoff", "safety"):
                if not isinstance(challenge.get(field), str) or len(challenge[field].strip()) < 12:
                    errors.append(f"{challenge_id}: missing or shallow {field}")
            if challenge.get("lane") not in LANES:
                errors.append(f"{challenge_id}: invalid lane")
            if challenge.get("difficulty") not in DIFFICULTIES:
                errors.append(f"{challenge_id}: invalid difficulty")
            stars = challenge.get("stars")
            if (
                isinstance(stars, bool)
                or not isinstance(stars, int)
                or stars not in STAR_TIER_NAMES
            ):
                errors.append(f"{challenge_id}: stars must be 1, 2, or 3")
            if challenge.get("lane") == "boss" and stars != 3:
                errors.append(f"{challenge_id}: boss must use the three-star tier")
            hours = challenge.get("estimated_hours")
            if isinstance(hours, bool) or not isinstance(hours, int) or hours < 8:
                errors.append(f"{challenge_id}: estimated_hours must be at least 8")
            for field, minimum in (
                ("deliverables", 3),
                ("constraints", 3),
                ("adversarial_cases", 3),
            ):
                values = challenge.get(field)
                if not isinstance(values, list) or len(values) < minimum:
                    errors.append(f"{challenge_id}: {field} needs at least {minimum} items")
                elif any(not isinstance(value, str) or len(value.strip()) < 8 for value in values):
                    errors.append(f"{challenge_id}: {field} contains a shallow item")
            acceptance = challenge.get("acceptance")
            if not isinstance(acceptance, list) or len(acceptance) < 4:
                errors.append(f"{challenge_id}: acceptance needs at least 4 criteria")
            else:
                criterion_ids: list[str] = []
                for criterion in acceptance:
                    if not isinstance(criterion, dict):
                        errors.append(f"{challenge_id}: acceptance criterion must be an object")
                        continue
                    criterion_id = criterion.get("id")
                    text = criterion.get("criterion")
                    if not isinstance(criterion_id, str) or not re.fullmatch(r"A[1-9][0-9]?", criterion_id):
                        errors.append(f"{challenge_id}: invalid acceptance id {criterion_id!r}")
                    else:
                        criterion_ids.append(criterion_id)
                    if not isinstance(text, str) or len(text.strip()) < 12:
                        errors.append(f"{challenge_id}: shallow acceptance criterion")
                if len(criterion_ids) != len(set(criterion_ids)):
                    errors.append(f"{challenge_id}: duplicate acceptance id")

            prerequisites = challenge.get("prerequisites")
            if not isinstance(prerequisites, list) or not prerequisites:
                errors.append(f"{challenge_id}: needs prerequisites")
            else:
                for requirement in prerequisites:
                    if requirement not in module_ids and requirement not in challenge_set:
                        errors.append(f"{challenge_id}: unknown prerequisite {requirement}")
                        continue
                    if requirement in challenge_set:
                        required_match = CHALLENGE_ID.fullmatch(requirement)
                        if match and required_match:
                            current_key = (match.group("stage"), int(match.group("number")))
                            required_key = (
                                required_match.group("stage"),
                                int(required_match.group("number")),
                            )
                            if required_key >= current_key:
                                errors.append(f"{challenge_id}: prerequisite {requirement} is not earlier")

    for number in range(1, 8):
        stage = f"{number:02d}"
        previous_boss = f"H{number - 1:02d}.08"
        stage_challenges = [
            challenge for challenge in all_challenges if challenge.get("stage") == stage
        ]
        if not any(
            previous_boss in challenge.get("prerequisites", [])
            for challenge in stage_challenges
        ):
            errors.append(
                f"challenge pack {stage}: no problem consumes previous boss {previous_boss}"
            )

    atlas = course.root / "vault" / "Challenge Atlas.md"
    if not atlas.is_file():
        errors.append("missing vault/Challenge Atlas.md")
    return errors


def _render_list(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def render_pack(pack: dict[str, Any]) -> str:
    lines = [
        "---",
        f'title: "Hard Track {pack["id"]} - {pack["title"]}"',
        f'tags: ["course", "challenge", "hard-track", "stage-{pack["id"]}"]',
        "---",
        "",
        f'# Hard Track {pack["id"]}: {pack["title"]}',
        "",
        str(pack["overview"]),
        "",
        f'**Entry gate:** {pack["entry_gate"]}',
        "",
        f'**Stage handoff:** {pack["stage_handoff"]}',
        "",
        "Use `python3 ftt challenge start ID` to create an evidence workspace. The",
        "checker replays positive and negative commands and verifies every claimed",
        "artifact by hash; it cannot replace the engineering judgment in the rubric.",
        "",
        "### Difficulty ladder",
        "",
        "- `*` — focused: one main artifact and a narrow adversarial campaign.",
        "- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.",
        "- `***` — boss-scale: integrates the stage and produces the handoff consumed later.",
        "",
    ]
    for challenge in pack["challenges"]:
        stars = int(challenge["stars"])
        lines.extend(
            [
                f'## {challenge["id"]} · {_markdown_stars(stars)} · {challenge["title"]}',
                "",
                f'**{STAR_TIER_NAMES[stars].title()} · {challenge["difficulty"].title()} · {challenge["estimated_hours"]}–{challenge["estimated_hours"] + max(4, challenge["estimated_hours"] // 2)} hours · {challenge["lane"]}**',
                "",
                f'**Prerequisites:** {", ".join(challenge["prerequisites"])}',
                "",
                str(challenge["brief"]),
                "",
                f'**Artifact:** {challenge["artifact"]}',
                "",
                "### Deliverables",
                "",
                *_render_list(challenge["deliverables"]),
                "",
                "### Constraints",
                "",
                *_render_list(challenge["constraints"]),
                "",
                "### Adversarial campaign",
                "",
                *_render_list(challenge["adversarial_cases"]),
                "",
                "### Acceptance evidence",
                "",
                *[
                    f'- **{criterion["id"]}:** {criterion["criterion"]}'
                    for criterion in challenge["acceptance"]
                ],
                "",
                f'**Handoff:** {challenge["handoff"]}',
                "",
                f'**Safety:** {challenge["safety"]}',
                "",
            ]
        )
    lines.extend(["## Primary references", ""])
    for source in pack["sources"]:
        lines.append(f'- [{source["title"]}]({source["url"]}) — {source["use"]}')
    lines.extend(["", "Return to [[Challenge Atlas]].", ""])
    return "\n".join(lines)


def render_atlas(catalog: ChallengeCatalog) -> str:
    challenge_count = len(catalog.challenges)
    total_hours = sum(int(item["estimated_hours"]) for item in catalog.challenges)
    lines = [
        "---",
        'title: "Challenge Atlas"',
        'tags: ["course", "map", "challenge", "hard-track"]',
        "---",
        "",
        "# Challenge Atlas",
        "",
        str(catalog.track["description"]),
        "",
        f"This is a {challenge_count}-problem advanced track (about {total_hours} base hours). It is",
        "deliberately separate from the C-beginner core. Do a stage after its normal gate,",
        "or return after the capstone and climb it as one cumulative systems gauntlet.",
        "",
        "## Operating rules",
        "",
        "1. For stage mastery, complete any six of the seven non-boss problems and then",
        "   its boss; complete all eight for the black track.",
        "2. Keep the oracle, generator, implementation, and corpus independently",
        "   replaceable. A second implementation is stronger evidence than more examples.",
        "3. Every completion packet needs a positive replay, a negative replay, artifact",
        "   hashes, the first divergent observation, an invariant, and known limitations.",
        "4. Preserve each boss artifact: the next stage consumes it.",
        "5. Physical work is never required to validate the software/simulation result.",
        "",
        "## Star ladder",
        "",
        "Stars describe dependency and integration scope, not whether a problem is easy:",
        "",
        "- `*` — focused hard problem; a good first challenge after the stage gate.",
        "- `**` — cumulative/adversarial problem; expects several contracts or an independent oracle.",
        "- `***` — stage boss; integrates the stage and freezes the next handoff.",
        "",
        "```sh",
        "python3 ftt challenge list",
        "python3 ftt challenge show H03.01",
        "python3 ftt challenge start H03.01",
        "python3 ftt challenge check H03.01",
        "```",
        "",
        "## Stages",
        "",
        "| Stage | Problems | Base hours | Cumulative handoff |",
        "|---|---:|---:|---|",
    ]
    for pack in catalog.packs:
        count = len(pack["challenges"])
        hours = sum(int(challenge["estimated_hours"]) for challenge in pack["challenges"])
        lines.append(
            f'| [[{Path(pack["path"]).stem}|{pack["id"]} {pack["title"]}]] | {count} | {hours} | {pack["stage_handoff"]} |'
        )
    lines.extend(
        [
            "",
            "## What the checker proves",
            "",
            "`ftt challenge check` executes learner-declared argv arrays without a shell,",
            "checks expected status/output fragments, confines artifact paths to the",
            "workspace, and verifies SHA-256 digests. Recorded completion becomes stale if",
            "that packet changes or disappears. This proves the submitted evidence is present",
            "and replayable. It does not prove an open-ended design is optimal, safe",
            "on arbitrary hardware, or free of bugs; use each problem's acceptance rubric",
            "and inspect a sampled trace or counterexample yourself. Replay is resource-bounded",
            "but not sandboxed; run only code you trust under your user account.",
            "",
            "Return to [[Course Map]] or [[Home]].",
            "",
        ]
    )
    return "\n".join(lines)


def render_challenge_brief(
    challenge: dict[str, Any], pack: dict[str, Any] | None = None
) -> str:
    lines = [
        f'# {challenge["id"]} · {_markdown_stars(int(challenge["stars"]))} · {challenge["title"]}',
        "",
        f'**{STAR_TIER_NAMES[int(challenge["stars"])].title()} · {challenge["difficulty"].title()} · about {challenge["estimated_hours"]} hours · {challenge["lane"]}**',
        "",
        f'Prerequisites: {", ".join(challenge["prerequisites"])}',
        "",
        str(challenge["brief"]),
        "",
        f'Artifact: {challenge["artifact"]}',
        "",
        "## Deliverables",
        "",
        *_render_list(challenge["deliverables"]),
        "",
        "## Constraints",
        "",
        *_render_list(challenge["constraints"]),
        "",
        "## Adversarial campaign",
        "",
        *_render_list(challenge["adversarial_cases"]),
        "",
        "## Acceptance",
        "",
        *[
            f'- **{criterion["id"]}:** {criterion["criterion"]}'
            for criterion in challenge["acceptance"]
        ],
        "",
        f'Handoff: {challenge["handoff"]}',
        "",
        f'Safety: {challenge["safety"]}',
        "",
    ]
    if pack is not None:
        lines.extend(
            [
                "## Stage contract",
                "",
                f'Entry gate: {pack["entry_gate"]}',
                "",
                f'Stage handoff: {pack["stage_handoff"]}',
                "",
                "## Primary references",
                "",
                *[
                    f'- [{source["title"]}]({source["url"]}) — {source["use"]}'
                    for source in pack["sources"]
                ],
                "",
            ]
        )
    return "\n".join(lines)


def start_challenge(
    catalog: ChallengeCatalog,
    challenge_id: str,
    destination: Path,
    *,
    force: bool = False,
) -> Path:
    challenge = catalog.challenge(challenge_id)
    pack = catalog.challenge_pack(challenge_id)
    destination = destination.expanduser().resolve()
    if destination.exists() and not destination.is_dir():
        raise CourseError(f"Challenge workspace path is not a directory: {destination}")
    marker = destination / ".ftt-challenge"
    if destination.exists() and any(destination.iterdir()):
        if not force:
            raise CourseError(f"Challenge workspace already exists and is not empty: {destination}")
        try:
            marker_value = marker.read_text(encoding="utf-8").strip()
        except (FileNotFoundError, OSError, UnicodeError) as exc:
            raise CourseError(
                f"Refusing --force outside a marked challenge workspace: {destination}"
            ) from exc
        if marker_value != challenge["id"]:
            raise CourseError(
                f"Refusing --force: workspace marker is {marker_value!r}, expected {challenge['id']}"
            )
    destination.mkdir(parents=True, exist_ok=True)
    marker.write_text(challenge["id"] + "\n", encoding="utf-8")
    (destination / "CHALLENGE.md").write_text(
        render_challenge_brief(challenge, pack), encoding="utf-8"
    )
    report = "\n".join(
        [
            f'# Report — {challenge["id"]}',
            "",
            "## Design and oracle",
            "",
            "TODO",
            "",
            "## First divergent observation",
            "",
            "TODO",
            "",
            "## Invariant",
            "",
            "TODO",
            "",
            "## Fault campaign and limitations",
            "",
            "TODO",
            "",
        ]
    )
    (destination / "REPORT.md").write_text(report, encoding="utf-8")
    acceptance = {criterion["id"]: [] for criterion in challenge["acceptance"]}
    evidence = {
        "schema_version": 1,
        "challenge_id": challenge["id"],
        "claim": {
            "invariant": "",
            "first_divergence": "",
            "limitations": "",
        },
        "artifacts": [
            {"path": "REPORT.md", "sha256": "REPLACE_WITH_SHA256"},
        ],
        "acceptance": acceptance,
        "replay": [
            {
                "name": "working path",
                "kind": "positive",
                "argv": [],
                "expected_exit": 0,
                "output_contains": [],
                "timeout_seconds": 30,
            },
            {
                "name": "adversarial path",
                "kind": "negative",
                "argv": [],
                "expected_exit": 0,
                "output_contains": [],
                "timeout_seconds": 30,
            },
        ],
    }
    (destination / "evidence.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )
    return destination


def _safe_artifact(work: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        raise CourseError(f"artifact path must be relative: {value}")
    resolved = (work / candidate).resolve()
    try:
        resolved.relative_to(work.resolve())
    except ValueError as exc:
        raise CourseError(f"artifact path escapes workspace: {value}") from exc
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _expand_argv(argv: list[str], root: Path, work: Path) -> list[str]:
    replacements = {
        "{python}": sys.executable,
        "{root}": str(root),
        "{work}": str(work),
        "{cc}": os.environ.get("CC", "cc"),
    }
    return [replacements.get(value, value) for value in argv]


def check_evidence(
    catalog: ChallengeCatalog,
    challenge_id: str,
    work: Path,
) -> EvidenceResult:
    challenge = catalog.challenge(challenge_id)
    work = work.expanduser().resolve()
    path = work / "evidence.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return EvidenceResult((f"missing evidence packet: {path}",), ())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return EvidenceResult((f"invalid evidence packet: {exc}",), ())
    if not isinstance(data, dict):
        return EvidenceResult(("evidence packet must be a JSON object",), ())

    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("evidence schema_version must be 1")
    if data.get("challenge_id") != challenge["id"]:
        errors.append(f"evidence challenge_id must be {challenge['id']}")
    claim = data.get("claim")
    if not isinstance(claim, dict):
        errors.append("claim must be an object")
    else:
        for field in ("invariant", "first_divergence", "limitations"):
            value = claim.get(field)
            if not isinstance(value, str) or len(value.strip()) < 24:
                errors.append(f"claim.{field} must contain at least 24 characters")

    artifact_paths: dict[str, Path] = {}
    resolved_artifacts: set[Path] = set()
    file_identities: set[tuple[int, int]] = set()
    expected_digests: dict[Path, str] = {}
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("artifacts must list at least two hashed files")
        artifacts = []
    elif len(artifacts) < 2:
        errors.append("artifacts must list at least two hashed files")
    for index, artifact in enumerate(artifacts, start=1):
        if not isinstance(artifact, dict):
            errors.append(f"artifact {index} must be an object")
            continue
        relative = artifact.get("path")
        expected = artifact.get("sha256")
        if not isinstance(relative, str):
            errors.append(f"artifact {index} needs a relative path")
            continue
        try:
            artifact_path = _safe_artifact(work, relative)
        except CourseError as exc:
            errors.append(str(exc))
            continue
        if relative in artifact_paths:
            errors.append(f"duplicate artifact path: {relative}")
            continue
        if artifact_path in resolved_artifacts:
            errors.append(f"artifact aliases another declared path: {relative}")
            continue
        artifact_paths[relative] = artifact_path
        resolved_artifacts.add(artifact_path)
        if not artifact_path.is_file():
            errors.append(f"artifact does not exist: {relative}")
            continue
        else:
            try:
                stat = artifact_path.stat()
            except OSError as exc:
                errors.append(f"artifact {relative}: could not stat: {exc}")
                continue
            identity = (stat.st_dev, stat.st_ino)
            if identity in file_identities:
                errors.append(f"artifact hard-links another declared file: {relative}")
                continue
            file_identities.add(identity)
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            errors.append(f"artifact {relative}: sha256 must be 64 lowercase hex characters")
        else:
            try:
                actual = _sha256(artifact_path)
            except OSError as exc:
                errors.append(f"artifact {relative}: could not hash: {exc}")
                continue
            if actual != expected:
                errors.append(f"artifact {relative}: sha256 mismatch")
            else:
                expected_digests[artifact_path] = expected
    if len(resolved_artifacts) < 2:
        errors.append("artifacts must resolve to at least two distinct files")
    if len(file_identities) < 2:
        errors.append("artifacts must identify at least two independently stored files")

    acceptance = data.get("acceptance")
    expected_criteria = {criterion["id"] for criterion in challenge["acceptance"]}
    if not isinstance(acceptance, dict) or set(acceptance) != expected_criteria:
        errors.append("acceptance keys must exactly match the challenge criteria")
    else:
        for criterion_id, references in acceptance.items():
            if not isinstance(references, list) or not references:
                errors.append(f"acceptance {criterion_id} needs at least one artifact path")
                continue
            for reference in references:
                if not isinstance(reference, str):
                    errors.append(
                        f"acceptance {criterion_id}: artifact references must be strings"
                    )
                elif reference not in artifact_paths:
                    errors.append(f"acceptance {criterion_id}: unknown artifact {reference!r}")

    replay_specs = data.get("replay")
    if not isinstance(replay_specs, list):
        errors.append("replay needs at least two commands")
        replay_specs = []
    elif len(replay_specs) < 2:
        errors.append("replay needs at least two commands")
    kinds = {item.get("kind") for item in replay_specs if isinstance(item, dict)}
    if kinds != REPLAY_KINDS:
        errors.append("replay must include both positive and negative commands")

    prepared_replays: list[dict[str, Any]] = []
    replay_names: set[str] = set()
    for index, replay in enumerate(replay_specs, start=1):
        if not isinstance(replay, dict):
            errors.append(f"replay {index} must be an object")
            continue
        name = replay.get("name")
        argv = replay.get("argv")
        expected_exit = replay.get("expected_exit")
        timeout = replay.get("timeout_seconds", 10)
        output_contains = replay.get("output_contains", [])
        if not isinstance(name, str) or not name.strip():
            errors.append(f"replay {index} needs a name")
            continue
        if name in replay_names:
            errors.append(f"duplicate replay name: {name}")
            continue
        replay_names.add(name)
        if replay.get("kind") not in REPLAY_KINDS:
            errors.append(f"replay {name}: kind must be positive or negative")
            continue
        if (
            not isinstance(argv, list)
            or not argv
            or any(not isinstance(value, str) for value in argv)
            or not argv[0]
            or any("\x00" in value for value in argv)
        ):
            errors.append(f"replay {name}: argv must be a non-empty string list")
            continue
        if isinstance(expected_exit, bool) or not isinstance(expected_exit, int):
            errors.append(f"replay {name}: expected_exit must be an integer")
            continue
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, int)
            or not 1 <= timeout <= MAX_REPLAY_TIMEOUT
        ):
            errors.append(
                f"replay {name}: timeout_seconds must be 1 through {MAX_REPLAY_TIMEOUT}"
            )
            continue
        if not isinstance(output_contains, list) or any(
            not isinstance(value, str) or not value for value in output_contains
        ):
            errors.append(f"replay {name}: output_contains must be a list of non-empty strings")
            continue
        prepared_replays.append(
            {
                "name": name,
                "argv": argv,
                "expected_exit": expected_exit,
                "timeout": timeout,
                "output_contains": output_contains,
            }
        )

    if errors:
        return EvidenceResult(tuple(errors), ())

    try:
        packet_digest = _sha256(path)
    except OSError as exc:
        return EvidenceResult((f"could not snapshot evidence packet: {exc}",), ())

    replays: list[ReplayResult] = []
    for replay in prepared_replays:
        name = replay["name"]
        command = _expand_argv(replay["argv"], catalog.root, work)
        try:
            completed = run_argv_limited(command, work, replay["timeout"])
            combined_output = completed.stdout
            failures: list[str] = []
            if completed.returncode != replay["expected_exit"]:
                failures.append(
                    f"exit {completed.returncode}, expected {replay['expected_exit']}"
                )
            if OUTPUT_TRUNCATED_MARKER in combined_output:
                failures.append("combined output exceeded the 1 MiB replay limit")
            for fragment in replay["output_contains"]:
                if fragment not in combined_output:
                    failures.append(f"output missing {fragment!r}")
            replays.append(ReplayResult(name, not failures, "; ".join(failures)))
        except (OSError, ValueError) as exc:
            replays.append(ReplayResult(name, False, str(exc)))
        except subprocess.TimeoutExpired:
            replays.append(
                ReplayResult(name, False, f"timed out after {replay['timeout']}s")
            )

    try:
        if not path.is_file() or _sha256(path) != packet_digest:
            errors.append("evidence packet changed during replay")
    except OSError as exc:
        errors.append(f"evidence packet could not be rechecked after replay: {exc}")
    for artifact_path, expected in expected_digests.items():
        try:
            if not artifact_path.is_file() or _sha256(artifact_path) != expected:
                errors.append(
                    f"artifact changed during replay: {artifact_path.relative_to(work)}"
                )
        except (OSError, ValueError) as exc:
            errors.append(f"artifact could not be rechecked after replay: {exc}")

    return EvidenceResult(tuple(errors), tuple(replays))

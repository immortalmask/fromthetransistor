---
title: "Challenge Atlas"
tags: ["course", "map", "challenge", "hard-track"]
---

# Challenge Atlas

Sixty-four unusual, cumulative systems problems that expand the runnable core toward the original transistor-to-browser ambition without claiming undocumented author intent or making unsafe physical work mandatory.

This is a 64-problem advanced track (about 2024 base hours). It is
deliberately separate from the C-beginner core. Do a stage after its normal gate,
or return after the capstone and climb it as one cumulative systems gauntlet.

## Operating rules

1. For stage mastery, complete any six of the seven non-boss problems and then
   its boss; complete all eight for the black track.
2. Keep the oracle, generator, implementation, and corpus independently
   replaceable. A second implementation is stronger evidence than more examples.
3. Every completion packet needs a positive replay, a negative replay, artifact
   hashes, the first divergent observation, an invariant, and known limitations.
4. Preserve each boss artifact: the next stage consumes it.
5. Physical work is never required to validate the software/simulation result.

## Star ladder

Stars describe dependency and integration scope, not whether a problem is easy:

- `*` — focused hard problem; a good first challenge after the stage gate.
- `**` — cumulative/adversarial problem; expects several contracts or an independent oracle.
- `***` — stage boss; integrates the stage and freezes the next handoff.

```sh
python3 ftt challenge list
python3 ftt challenge show H03.01
python3 ftt challenge start H03.01
python3 ftt challenge check H03.01
```

## Stages

| Stage | Problems | Base hours | Cumulative handoff |
|---|---:|---:|---|
| [[00 Hostile C and Binary Forensics|00 Hostile C and Binary Forensics]] | 8 | 172 | A capsule-v1 replay format, libbyte artifact, minimized corpus, and reproducible-build manifest consumed by every later stage. |
| [[01 Logic Under Cross-Examination|01 Logic Under Cross-Examination]] | 8 | 198 | A simtrace-v1 edge schema, synthesizable clockwork block, C logic oracle, mutation report, and reset contract. |
| [[02 Bringup Through Hostile Wires|02 Bringup Through Hostile Wires]] | 8 | 198 | A bus-v1 register contract, cycle-accurate UART, recovery console, and transaction corpus. |
| [[03 ISA CPU and Hostile Boot|03 ISA CPU and Hostile Boot]] | 8 | 270 | A versioned ISA, assembler corpus, CPU trace ABI, boot monitor, and independently checked ROM repair. |
| [[04 Toolchain That Must Survive Itself|04 Toolchain That Must Survive Itself]] | 8 | 278 | A reproducible C0 toolchain, target ABI, ELF profile, runtime, NIC contract, and boot bundle. |
| [[05 Kernel and Storage Failure Laboratory|05 Kernel and Storage Failure Laboratory]] | 8 | 302 | A syscall ABI, deterministic kernel trace, kernel ELF, disposable root image, and power-failure corpus. |
| [[06 Network and Browser in an Adversarial Box|06 Network and Browser in an Adversarial Box]] | 8 | 296 | A network adversary, TCP corpus, optional sealed loader, browser image, and packet-to-render trace. |
| [[07 Evidence-First Physical Bringup|07 Evidence-First Physical Bringup]] | 8 | 310 | A reviewed board pack, read-only flash transcript, three-way concordance report, rollback image, and bringup capsule. |

## What the checker proves

`ftt challenge check` executes learner-declared argv arrays without a shell,
checks expected status/output fragments, confines artifact paths to the
workspace, and verifies SHA-256 digests. Recorded completion becomes stale if
that packet changes or disappears. This proves the submitted evidence is present
and replayable. It does not prove an open-ended design is optimal, safe
on arbitrary hardware, or free of bugs; use each problem's acceptance rubric
and inspect a sampled trace or counterexample yourself. Replay is resource-bounded
but not sandboxed; run only code you trust under your user account.

Return to [[Course Map]] or [[Home]].

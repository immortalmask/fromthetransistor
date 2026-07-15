---
title: "Learner Guide"
tags: ["course", "guide"]
---

# Learner Guide

This is a construction course, not a reading list. Work in short loops: predict observable behavior, run the smallest experiment, locate the first disagreement, change one cause, and preserve evidence.

## Before each session

```sh
git status --short
python3 ftt next
python3 ftt show 00.01
```

Replace `00.01` with the active module. Read its exit criteria before doing the homework; that keeps “done” tied to an artifact rather than time spent.

Each module ends with two to four English external sources chosen for that
module's workbook or homework. Start with the item marked **Start here**. Open a
**Reference** only when you need an exact contract, encoding, API, or state
transition; use **Go deeper** after the core artifact works. The same links are
indexed in [[Reference Shelf]]. This is a lookup layer around the practical
course, not prerequisite reading to finish before coding.

Create learner lab work with the course runner instead of editing starter or solution assets:

```sh
python3 ftt start MODULE_ID
python3 ftt check MODULE_ID
```

The first command applies only to modules with an automated lab. By default it creates a working copy under `work/`. The check records evidence when it passes. Read the lab's local instructions before changing files.

The workspace also contains `tests/test.c`, `test_support.h`, and a `Makefile`.
These are native C black-box tests: the harness compiles `main.c` as a separate
program, sends it command-line arguments or raw stdin bytes, and compares its
exit status and output. Run them without the Python course runner:

```sh
cd work/LAB_ID
make test
```

The repository copy lives at `labs/LAB_ID/tests/test.c`; from the repository
root, `make c-tests` compiles and runs all twelve native suites. The JSON cases
used by `ftt check` and the C cases are synchronized automatically. Use the C
suite for the immediate edit/compile/test loop and `ftt check` when you also
want course-level resource limits, progress recording, and structured output.

Each started lab contains `LAB.md` plus a writable `WORKBOOK.md`. The workbook
is for predictions, hand traces, experiments, and the first-wrong-state debugging
record; it is evidence, not generated scratch text. For non-lab work or a vault
journal, copy [[Workbook Entry]], [[Lab Report]], or [[Exam Retrospective]].

For modules without an automated lab, record a concise manual completion statement:

```sh
python3 ftt complete MODULE_ID --evidence "artifact path; test command; observed result"
```

Evidence should be independently checkable. “Read the chapter” and “seems to work” are not evidence.

## Using the hard track

After a normal stage gate, open [[Challenge Atlas]] and choose several problems
rather than treating its boss as the only exercise. A challenge workspace is an
evidence shell, not a starter solution:

- begin with a `*` focused problem;
- move to `**` when you can preserve and compose the stage contracts;
- attempt the `***` boss only after the required handoffs replay cleanly.

```sh
python3 ftt challenge list --stage 03
python3 ftt challenge show H03.01
python3 ftt challenge start H03.01
python3 ftt challenge check H03.01
```

Fill `evidence.json` only with paths inside the workspace. Hash at least two
artifacts, map every acceptance criterion to those artifacts, and declare at
least one positive and one negative replay as argument arrays. The runner does
not evaluate shell text. It checks hashes, expected exit status, output
fragments, timeouts, and the required written claims about the invariant, first
divergence, and limitations.

A passing packet is recorded only when its prerequisites are complete. If you
are deliberately investigating out of order, add `--waive-prerequisites`; the
waiver is stored with progress instead of silently pretending the dependency
was met. Challenge lists show `[!]` when a recorded evidence packet was deleted
or changed after its successful replay.

Replay is resource-bounded orchestration, not a security sandbox. Commands run
with your user permissions and may still access the network or files those
permissions allow. Declare and replay only code you trust; keep the course's
fixture/loopback safety rules even when the operating system would permit more.

Use a deterministic seed and case count for fuzz/property evidence. Keep
unknown target code in an emulator, networks on fixtures or loopback, disk work
on disposable images, and physical writes disabled until a reviewed bringup
gate explicitly permits them.

## The five-pass study loop

1. **Predict.** Write expected bytes, register values, state, output, and failure behavior before running anything.
2. **Trace.** Capture the smallest useful trace: expression table, debugger frame, waveform cycles, architectural states, syscalls, sectors, or packets.
3. **Implement.** Change one contract at a time. Prefer small named functions and explicit bounds.
4. **Attack.** Test zero, one, maximum, just-over-maximum, malformed, repeated, and interrupted cases.
5. **Explain.** State the invariant, the first divergent observation, and why the repair restores the invariant.

## A useful debugging ladder

Do not jump straight to the highest layer. Ask in order:

1. Are the input bytes what I think they are?
2. Is their width, signedness, alignment, and byte order explicit?
3. Is the state transition legal at this cycle or instruction?
4. Did control cross an ABI, MMIO, syscall, filesystem, or packet boundary?
5. Which side owns the buffer now, and for how long?
6. What is the first trace row where expected and actual state differ?

If the first divergence is unknown, collect a narrower trace. Adding random logging everywhere usually hides ordering and boundary mistakes.

## Working safely in C

- Compile learner C with strict warnings and sanitizers on the host whenever possible.
- Carry buffer pointer and length together. A pointer does not encode bounds.
- Check arithmetic before allocating, indexing, advancing a cursor, or converting width.
- Decode wire and disk formats byte-by-byte; do not cast untrusted bytes to a host struct.
- Give every allocated resource one documented owner and one cleanup path.
- Treat `volatile` only as an access property for MMIO; it is not synchronization.
- Assertions protect internal invariants. Validation handles hostile external input.

## Keeping evidence

For each module, retain:

- the command and revision that produced the result;
- one passing trace and one meaningful failing trace;
- a short artifact note: interface, invariant, limitations, and next dependency;
- any fixed random seed or fixture required to replay a failure.

Do not commit secrets, huge generated traces, copied proprietary HDL, or downloaded binaries of unknown provenance. Prefer a small fixture generator and its expected hash.

Inspect progress and exams with:

```sh
python3 ftt progress
python3 ftt exam list
python3 ftt exam gate-00
```

## Recovery when stuck

Reduce the system to the last trusted boundary. For a browser failure, first replay the HTML fixture without networking; then replay a saved HTTP response; then a TCP segment sequence; then packet/MMIO traces. For a boot failure, run the same bytes in the CPU model, inspect the first divergent instruction, and only then inspect the UART protocol.

After three unfocused attempts, stop changing code. Write down expected state, actual state, and the earliest known divergence. That note is usually more valuable than another speculative patch.

Return to [[Home]], use [[Course Map]] to check whether a missing prerequisite
explains the difficulty, or consult the active task's entry in [[Reference Shelf]].

When the section gates are complete, use [[Capstone - Browser in a Box|Browser
in a Box]] to integrate the verified boundaries without collapsing every layer
into one untraceable program.

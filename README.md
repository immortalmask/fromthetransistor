# From the Transistor to the Web Browser

![From the Transistor to the Web Browser](main.jpeg)

[![Build and test](https://github.com/immortalmask/fromthetransistor/actions/workflows/verify.yml/badge.svg?branch=master)](https://github.com/immortalmask/fromthetransistor/actions/workflows/verify.yml) [![Lint and consistency](https://github.com/immortalmask/fromthetransistor/actions/workflows/lint.yml/badge.svg?branch=master)](https://github.com/immortalmask/fromthetransistor/actions/workflows/lint.yml)

This is a course about building enough of a computer that its abstractions stop
feeling magical. You begin with C, bytes, and state machines; then build upward
through logic, devices, a small processor, a toolchain, an operating-system
model, networking, and a text browser.

The course is meant for someone who is curious about reverse engineering and
low-level systems but is not yet comfortable in C. The required path runs on an
ordinary Linux machine. An FPGA is optional.

The original Geohot outline is extremely ambitious. This repository does not
pretend that twelve tiny exercises equal an ARM CPU, compiler, Unix, TCP stack,
and physical board. Instead it provides two connected paths:

- **Core course:** 32 guided modules, 12 tested C labs, seven gates, five
  cumulative notebooks, lectures, workbooks, homework, and references.
- **Hard track:** 64 long-form systems problems involving binary archaeology,
  fuzzing, mutation testing, independent oracles, hostile boot/storage/network
  conditions, and cross-stage boss artifacts.

Start with the core. Use the hard track after you understand the corresponding
stage—or when the core version feels too polite.

## What you need

- Python 3.11 or newer
- a C17 compiler available as `cc` (Clang or GCC)
- GNU Make
- Git, recommended for checkpointing your work

No Python packages are required for the core runner. Jupyter is optional if you
want to open the notebooks interactively; their automated checks use only the
standard library.

## Your first session

From the repository root:

```sh
python3 ftt doctor
python3 ftt validate
python3 ftt list
python3 ftt show 00.01
```

`doctor` checks the course and your local tools. `show 00.01` prints the first
lesson. You can also open [`vault/Home.md`](vault/Home.md), or open the entire
[`vault/`](vault/) directory as an Obsidian vault. No Obsidian plugins are
required.

Do modules `00.01` through `00.03` before the first automated C lab. They cover
the build/debug loop and the C behavior that later looks deceptively like a CPU
or kernel bug.

When you reach `00.04`, start a real learner workspace:

```sh
python3 ftt start 00.04
cd work/lab-00-bytes
make test
```

The first test run is expected to fail: the starter compiles, but it is not the
solution. Read `LAB.md` and `WORKBOOK.md`, make predictions, then edit `main.c`.
Stay in the short loop:

```sh
make test
```

When the native C tests pass, return to the repository and run the course-level
checker:

```sh
cd ../..
python3 ftt check 00.04
python3 ftt progress
python3 ftt next
```

The course pages are source material; your code lives under ignored `work/`, and
your progress lives under ignored `.ftt/`. You can experiment without dirtying
the authored course.

## The normal work loop

At the start of a study session:

```sh
git status --short
python3 ftt next
python3 ftt show MODULE_ID
```

Then:

1. Read the exit criteria before coding.
2. Predict the bytes, state, trace, or failure you expect.
3. For a lab module, run `python3 ftt start MODULE_ID`, then work inside the
   generated directory with `make test`.
4. Run `python3 ftt check MODULE_ID` when the local loop passes.
5. Keep one meaningful failing trace, the repaired trace, and a short statement
   of the invariant that makes the repair correct.

Some modules intentionally have no bounded lab because their real assignment is
larger than one command-line program. Record those only after producing an
inspectable artifact:

```sh
python3 ftt complete 03.03 \
  --evidence "work/boot-monitor; make test; all truncation offsets rejected"
```

“Read the page” and “seems to work” are not completion evidence.

## What you build

| Stage | Result |
|---|---|
| 00 — C Runway | C debugging habits, explicit byte layouts, ownership, ABI inspection, and state machines |
| 01 — Logic | LUTs, registers, deterministic clocks, assertions, and waveform reasoning |
| 02 — Bringup | LED timing, UART framing, FIFO behavior, and an MMIO boundary |
| 03 — Processor | A fixed ISA, assembler, CPU model, trace contract, and boot monitor |
| 04 — Toolchain | A C subset, relocation/linking, allocator/runtime, packet device, and checked boot image |
| 05 — Operating System | Page translation, processes/syscalls, block faults, FAT, and small userland |
| 06 — Browser | Scoped TCP exercises, concurrent sessions, loading concepts, HTTP/HTML, and terminal rendering |
| 07 — Physical | JTAG, board review, fault isolation, and simulation-first bringup; live hardware remains optional |

The scaffolded core is roughly 404 hours. For a learner who is also learning C,
12–15 focused hours per week means about 36 weeks. Treat the historical
twelve-week estimate as a statement of intensity, not a sensible deadline.

## Workbooks, references, notebooks, and exams

Every module contains a compact lecture, prediction workbook, problem set,
cumulative homework, reverse-engineering lens, task-specific English sources,
and observable exit criteria.

- [`vault/Reference Shelf.md`](vault/Reference%20Shelf.md) collects the external
  manuals, specifications, courses, and deeper readings. Use the source attached
  to the current task; do not try to read the shelf front to back.
- [`vault/Notebook Guide.md`](vault/Notebook%20Guide.md) connects five executable
  analyses from byte contracts through CPU/toolchain/system integration and
  simulation-first bringup.
- `python3 ftt exam list` shows the seven gates. Each gate combines objective
  questions with a practical investigation; the quiz score alone is not enough.

## The hard track

Open [`vault/Challenge Atlas.md`](vault/Challenge%20Atlas.md) after completing a
stage gate. It contains eight problems per stage—seven independent lanes and one
boss—for 64 problems and about 2,024 base hours in total.

The stars make each stage a ladder rather than a flat wall:

- `*` — focused hard problem; start here after the stage gate;
- `**` — cumulative or adversarial work involving several contracts or an
  independent oracle;
- `***` — the stage boss, which integrates the block and produces its handoff.

A one-star challenge is still hard. The marker describes scope and dependency,
not an absolute promise about how many evenings it will take.

```sh
python3 ftt challenge list --stage 03
python3 ftt challenge show H03.01
python3 ftt challenge start H03.01
python3 ftt challenge check H03.01
```

A challenge workspace asks for real evidence: at least two independently stored
hashed artifacts, positive and negative replay commands, every acceptance
criterion mapped to evidence, the first divergence, an invariant, and known
limitations. Replay is resource-bounded but is **not a security sandbox**; run
only code you trust.

The checker refuses to record an out-of-order completion unless you explicitly
pass `--waive-prerequisites`. If a recorded evidence packet later changes or
disappears, challenge progress marks it stale with `[!]`.

The hard track is a rigorous project specification and validation protocol. It
is not 64 pre-solved labs. That distinction, the measured baseline, and the
comparison with the historical repository are documented in
[`Depth Audit and Geohot Alignment`](vault/Appendices/Depth%20Audit%20and%20Geohot%20Alignment.md).

## Useful commands

```text
python3 ftt doctor                     check authored content and local tools
python3 ftt list [--section 03]        list the core path
python3 ftt show 03.02                 print a module page
python3 ftt next                       show the next unlocked core module
python3 ftt start 03.02                create a learner lab workspace
python3 ftt check 03.02                compile, test, and record a passing lab
python3 ftt check --all-solutions      test every reference implementation
python3 ftt complete ID --evidence ... record a non-lab artifact
python3 ftt progress [--json]          show core and hard-track evidence
python3 ftt exam list                  list the assessment gates
python3 ftt validate                   validate the authored course
python3 ftt challenge list             list all hard problems
python3 ftt challenge show H05.07      print one hard problem
python3 ftt challenge start H05.07     create its evidence workspace
python3 ftt challenge check H05.07     verify and replay its evidence packet
```

Set `FTT_WORK_DIR` to move learner work, `FTT_STATE_DIR` to move progress, or
`CC` to select a compiler.

## When something goes wrong

- Run `python3 ftt doctor` when the checkout or toolchain seems wrong.
- Run the smallest local `make test` before the whole course checker.
- Find the first wrong byte, cycle, instruction, syscall, sector, or packet;
  later symptoms are usually noise.
- If a lab workspace becomes disposable, create a new destination rather than
  editing the checked-in starter or solution.
- The network exercises use fixtures or loopback. Never expose the teaching
  telnet service publicly.
- Physical work is optional. Do not connect unknown voltages, write unknown
  flash, or power an unreviewed board merely to satisfy a course checkbox.

## Repository map

```text
course/      catalogs, exams, references, and challenge specifications
labs/        12 C labs; each has starter, solution, lab.json, and tests/test.c
src/ftt/     course runner, validation, progress, and evidence machinery
tests/       tests for the runner and authored course
tools/       synchronization, notebook, sanitizer, and content checks
vault/       the Obsidian-ready lectures, workbooks, maps, and notebooks
work/        your generated learner work; ignored by Git
.ftt/        your local progress/evidence index; ignored by Git
```

## Course development

The repository should be releasable with one command:

```sh
make verify
```

That validates authored links and data, executes 50 Python tests, checks all 12
reference solutions, runs 119 co-located native C cases, executes the five
cumulative notebooks, and rebuilds/runs the C solutions with undefined-behavior
instrumentation.

For one lab's native suite:

```sh
make -C labs/lab-00-bytes test
make -C labs/lab-00-bytes test \
  SOURCE="$PWD/work/lab-00-bytes/main.c"
```

Authoring rules live in [`course/AUTHORING.md`](course/AUTHORING.md). The
historical mapping and deliberate adaptations are in
[`vault/Appendices/Original Syllabus.md`](vault/Appendices/Original%20Syllabus.md),
[`vault/Appendices/Scope Decisions.md`](vault/Appendices/Scope%20Decisions.md),
and [`vault/Appendices/realhw Branch Study.md`](vault/Appendices/realhw%20Branch%20Study.md).

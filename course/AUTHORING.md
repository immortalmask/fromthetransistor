# Course authoring contract

The catalog, vault pages, lab specifications, and exams are all checked data.
Run `python3 ftt validate` after changing any of them.

## Source of truth

- `course/catalog.json` owns section/module order, prerequisites, paths, lab
  associations, and exam associations.
- `course/source-outline.json` records every bullet from the original syllabus.
  Every source item must map to exactly one `01`–`07` module.
- `vault/` owns the instructional prose. Module pages use a tiny,
  JSON-compatible YAML frontmatter subset so the CLI needs no YAML dependency.
- `labs/<id>/lab.json` owns the CLI-facing public build and test contract.
  `labs/<id>/tests/test.c` mirrors every named case as a native C black-box
  suite. Learner code is executed as a separate process; it is never imported
  into either checker.
- `course/exams/<id>.json` owns the automatically graded knowledge questions;
  the matching vault page owns the practical investigation and rubric.
- `course/references.json` owns the verified external learning sources and their
  task-specific purpose. Run `python3 tools/sync_references.py` after changing it.
- `course/challenges.json` owns the 64-problem advanced track. Its eight pack
  pages and `vault/Challenge Atlas.md` are rendered by
  `python3 tools/sync_challenges.py`; `--check` rejects drift.

## Required module shape

Each catalog module points to one Markdown page with frontmatter containing at
least matching `id`, plus these exact level-two headings:

```markdown
## Why this block exists
## Lecture
## Workbook
## Problem set
## Homework
## Reverse-engineering lens
## External sources
## Exit criteria
```

Teach the normal path, edge conditions, and at least one invariant. Workbook
prompts should make the learner predict before running. Homework must name an
artifact and observable completion evidence rather than a line-count target.

## Lab format

Every lab contains:

```text
labs/<id>/
  Makefile
  README.md
  lab.json
  starter/
  solution/
  tests/test.c
```

`lab.json` contains an argv-array build step and argv-array test cases. Tokens
supported by the runner are `{cc}`, `{python}`, `{root}`, `{work}`, and
`{build}`. No string is evaluated by a shell. Expected output should be stable,
short, locale-independent, and offline.

The C suite uses the shared `labs/test_support.h` process harness and must carry
the same case names, arguments, input bytes, exit codes, output, and comparison
mode as `lab.json`. Run `python3 tools/sync_native_c_tests.py` after changing a
case; `--check` and `make c-tests` reject drift between the two declarations.
From the lab directory, `make test` checks `solution/main.c`; pass an absolute
`SOURCE=/path/to/main.c` to check learner code.

Starter code must compile cleanly under its declared flags while failing at
least one behavioral check. The reference solution must pass every public
check. Use fixed-width integers for encoded formats and decode bytes explicitly
instead of casting untrusted buffers to C structs.

## Adding content

1. Add or update the catalog entry and its prerequisites.
2. Create the vault page and required headings.
3. If practical automation helps, add a lab and associate its ID in the module.
4. Add assessment questions only when their explanations teach why alternatives
   fail.
5. Add two to four task-specific sources in `course/references.json`, then run
   `python3 tools/sync_references.py`.
6. Run `python3 ftt validate`, `python3 ftt check --all-solutions`, `make
   c-tests`, and the unit tests. The tests also prove that native/JSON cases,
   generated source blocks, and the shelf remain synchronized.

## Hard-problem format

Each stage has exactly eight distinct problems and one boss. A challenge names a
nontrivial artifact, earlier module/challenge prerequisites, three deliverables,
three constraints, three adversarial cases, four acceptance criteria, a later
handoff, and a safety boundary. Prefer a differential oracle, invariant,
mutation score, exhaustive bounded schedule, or deterministic generated corpus
over a longer list of examples.

Every stage has two `*` focused problems, five `**` cumulative/adversarial
problems, and one `***` boss. Stars describe integration scope, not whether the
underlying systems topic is objectively easy. The boss must be the final
challenge and must freeze an artifact consumed by the next stage.

The common evidence packet has at least two SHA-256-addressed artifacts and two
replay commands: one positive and one negative. Commands are argument arrays,
never shell strings, and time out after at most 120 seconds. Output, address
space, file size, open files, and process lifetime are bounded (1 MiB captured
output, 4 GiB address space, 256 MiB per file, and 256 open descriptors). The checker
validates replayability; it does not confer correctness on an open engineering
claim and is not a sandbox for hostile code.

## External-source policy

Every module and the capstone have two to four external sources: at least one
approachable `Start here` item, an exact manual/specification when useful, and a
deeper extension when useful. Prefer standards bodies, official project/tool
manuals, original university course material, RFCs, and vendor documentation.
A link must say which workbook or homework decision it helps with; generic
reading lists are not accepted.

Update `verified_on` when links are rechecked, then run:

```sh
python3 tools/sync_references.py
python3 tools/sync_references.py --check
```

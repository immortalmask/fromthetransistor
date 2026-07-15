---
title: "Hard Track 00 - Hostile C and Binary Forensics"
tags: ["course", "challenge", "hard-track", "stage-00"]
---

# Hard Track 00: Hostile C and Binary Forensics

Turn the C runway into a forensic laboratory where formats, lifetimes, ABI boundaries, state machines, and build evidence must survive hostile inputs.

**Entry gate:** Complete modules 00.01 through 00.08 and pass gate-00 before starting the boss.

**Stage handoff:** A capsule-v1 replay format, libbyte artifact, minimized corpus, and reproducible-build manifest consumed by every later stage.

Use `python3 ftt challenge start ID` to create an evidence workspace. The
checker replays positive and negative commands and verifies every claimed
artifact by hash; it cannot replace the engineering judgment in the rubric.

### Difficulty ladder

- `*` — focused: one main artifact and a narrow adversarial campaign.
- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.
- `***` — boss-scale: integrates the stage and produces the handoff consumed later.

## H00.01 · \* · Binary Palimpsest

**Focused · Very Hard · 18–27 hours · archaeology**

**Prerequisites:** 00.04

Infer a mixed-endian checksummed format from specimens, then implement a strict C decoder and inverse encoder.

**Artifact:** C codec, recovered schema, and specimen corpus

### Deliverables

- A working C codec, recovered schema, and specimen corpus with reproducible build and invocation instructions.
- A deterministic oracle or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with hashes, first divergence, invariant, and known limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit resource bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- Validate bounded data before mutation or output and keep raw evidence immutable.

### Adversarial campaign

- one-bit checksum mutation
- truncated multibyte field
- bytes defeating host-endian casts

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial case replays and invalid input becomes a typed failure rather than a crash or hang.
- **A3:** Evidence records seed, tool versions, hashes, first divergence, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented conversion or manual repair.

**Handoff:** The schema and codec become the byte-boundary library for capsule-v1.

**Safety:** Run unknown bytes only through bounded parsers or the course machine; sanitizers are diagnostics, not a hostile-code sandbox.

## H00.02 · \* · ABI Doppelganger

**Focused · Brutal · 22–33 hours · archaeology**

**Prerequisites:** 00.07, H00.01

Inspect immutable object files with incompatible layout or calling assumptions and build the smallest C or assembly shim.

**Artifact:** ABI shim, annotated disassembly, and relocation report

### Deliverables

- A working ABI shim, annotated disassembly, and relocation report with reproducible build and invocation instructions.
- A deterministic oracle or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with hashes, first divergence, invariant, and known limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit resource bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- Validate bounded data before mutation or output and keep raw evidence immutable.

### Adversarial campaign

- callee-saved register clobber
- padded structure with wrong layout
- symbol resolving to wrong section

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial case replays and invalid input becomes a typed failure rather than a crash or hang.
- **A3:** Evidence records seed, tool versions, hashes, first divergence, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented conversion or manual repair.

**Handoff:** The call trace seeds compiler and linker ABI tests.

**Safety:** Run unknown bytes only through bounded parsers or the course machine; sanitizers are diagnostics, not a hostile-code sandbox.

## H00.03 · \*\* · Lifetime Crime Scene

**Cumulative · Very Hard · 20–30 hours · adversary**

**Prerequisites:** 00.06

Minimize and repair use-after-free, double-free, and leak faults hidden behind an opaque library.

**Artifact:** repaired C client, fail-at-N allocator, and ownership traces

### Deliverables

- A working repaired C client, fail-at-N allocator, and ownership traces with reproducible build and invocation instructions.
- A deterministic oracle or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with hashes, first divergence, invariant, and known limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit resource bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- Validate bounded data before mutation or output and keep raw evidence immutable.

### Adversarial campaign

- failure after each allocation
- partial initialization cleanup
- alias outliving its owner

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial case replays and invalid input becomes a typed failure rather than a crash or hang.
- **A3:** Evidence records seed, tool versions, hashes, first divergence, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented conversion or manual repair.

**Handoff:** The failure injector is reused by runtime and kernel work.

**Safety:** Run unknown bytes only through bounded parsers or the course machine; sanitizers are diagnostics, not a hostile-code sandbox.

## H00.04 · \*\* · Bitstream Courier

**Cumulative · Very Hard · 18–27 hours · construction**

**Prerequisites:** 00.04, H00.01

Build a bounded bit reader and writer for cross-byte fields in both bit orders without undefined shifts.

**Artifact:** portable C bitstream library, oracle, and corpus

### Deliverables

- A working portable C bitstream library, oracle, and corpus with reproducible build and invocation instructions.
- A deterministic oracle or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with hashes, first divergence, invariant, and known limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit resource bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- Validate bounded data before mutation or output and keep raw evidence immutable.

### Adversarial campaign

- 32-bit field at final legal bit
- zero-capacity destination
- opposite orders over same bytes

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial case replays and invalid input becomes a typed failure rather than a crash or hang.
- **A3:** Evidence records seed, tool versions, hashes, first divergence, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented conversion or manual repair.

**Handoff:** The codec feeds serial, ISA, packet, and JTAG fields.

**Safety:** Run unknown bytes only through bounded parsers or the course machine; sanitizers are diagnostics, not a hostile-code sandbox.

## H00.05 · \*\* · State-Machine Witness

**Cumulative · Brutal · 24–36 hours · archaeology**

**Prerequisites:** 00.08

Recover the smallest Mealy machine consistent with incomplete traces and construct distinguishing sequences.

**Artifact:** table-driven C machine, inference report, and minimality certificate

### Deliverables

- A working table-driven C machine, inference report, and minimality certificate with reproducible build and invocation instructions.
- A deterministic oracle or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with hashes, first divergence, invariant, and known limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit resource bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- Validate bounded data before mutation or output and keep raw evidence immutable.

### Adversarial campaign

- states separated by long suffix
- trace ending before output
- nonminimal candidate

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial case replays and invalid input becomes a typed failure rather than a crash or hang.
- **A3:** Evidence records seed, tool versions, hashes, first divergence, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented conversion or manual repair.

**Handoff:** The inferred-machine schema becomes the logic black-box oracle.

**Safety:** Run unknown bytes only through bounded parsers or the course machine; sanitizers are diagnostics, not a hostile-code sandbox.

## H00.06 · \*\* · Length-Field Siege

**Cumulative · Brutal · 24–36 hours · adversary**

**Prerequisites:** 00.05, H00.04

Implement an iterative nested TLV parser whose progress, depth, arithmetic, and output remain bounded.

**Artifact:** bounded C parser, grammar generator, and rejection corpus

### Deliverables

- A working bounded C parser, grammar generator, and rejection corpus with reproducible build and invocation instructions.
- A deterministic oracle or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with hashes, first divergence, invariant, and known limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit resource bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- Validate bounded data before mutation or output and keep raw evidence immutable.

### Adversarial campaign

- length wrapping with header
- maximum-depth empty containers
- child extending beyond parent

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial case replays and invalid input becomes a typed failure rather than a crash or hang.
- **A3:** Evidence records seed, tool versions, hashes, first divergence, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented conversion or manual repair.

**Handoff:** The budgets and minimizer become the hostile-input harness.

**Safety:** Run unknown bytes only through bounded parsers or the course machine; sanitizers are diagnostics, not a hostile-code sandbox.

## H00.07 · \*\* · Reproducibility Autopsy

**Cumulative · Very Hard · 16–24 hours · archaeology**

**Prerequisites:** 00.02, 00.07

Diagnose path, time, locale, and input-order nondeterminism until independent builds produce identical bytes.

**Artifact:** repaired build, two-environment transcript, and hash manifest

### Deliverables

- A working repaired build, two-environment transcript, and hash manifest with reproducible build and invocation instructions.
- A deterministic oracle or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with hashes, first divergence, invariant, and known limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit resource bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- Validate bounded data before mutation or output and keep raw evidence immutable.

### Adversarial campaign

- different checkout roots
- different locale and timezone
- shuffled archive members

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial case replays and invalid input becomes a typed failure rather than a crash or hang.
- **A3:** Evidence records seed, tool versions, hashes, first divergence, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented conversion or manual repair.

**Handoff:** The manifest and clean-room probe are required by later bosses.

**Safety:** Run unknown bytes only through bounded parsers or the course machine; sanitizers are diagnostics, not a hostile-code sandbox.

## H00.08 · \*\*\* · Boss: Evidence Capsule

**Boss-Scale · Brutal · 30–45 hours · boss**

**Prerequisites:** H00.01, H00.05, H00.06, H00.07

Create capsule-v1 for input, seed, expected trace, hashes, and replay metadata, rejecting corruption before replay.

**Artifact:** versioned capsule tool, replay engine, schema, and corruption corpus

### Deliverables

- A working versioned capsule tool, replay engine, schema, and corruption corpus with reproducible build and invocation instructions.
- A deterministic oracle or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with hashes, first divergence, invariant, and known limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit resource bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- Validate bounded data before mutation or output and keep raw evidence immutable.

### Adversarial campaign

- truncated manifest
- artifact digest mismatch
- workspace-escaping path

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial case replays and invalid input becomes a typed failure rather than a crash or hang.
- **A3:** Evidence records seed, tool versions, hashes, first divergence, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented conversion or manual repair.

**Handoff:** capsule-v1 becomes the cross-stage evidence transport.

**Safety:** Run unknown bytes only through bounded parsers or the course machine; sanitizers are diagnostics, not a hostile-code sandbox.

## Primary references

- [WG14 N2176 C17 draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2176.pdf) — Define integer, lifetime, representation, and undefined-behavior boundaries for every C artifact.
- [System V ABI ELF specification](https://gabi.xinuos.com/) — Ground object, symbol, section, relocation, and ABI investigations in the executable-format contract.
- [Clang AddressSanitizer documentation](https://clang.llvm.org/docs/AddressSanitizer.html) — Configure reproducible memory-safety evidence without treating instrumentation as a proof.
- [Reproducible Builds documentation](https://reproducible-builds.org/docs/) — Design two-root and two-time experiments and record every input affecting output hashes.

Return to [[Challenge Atlas]].

---
title: "Hard Track 01 - Logic Under Cross-Examination"
tags: ["course", "challenge", "hard-track", "stage-01"]
---

# Hard Track 01: Logic Under Cross-Examination

Build independent C and RTL models, then attack reset, timing, handshake, and waveform assumptions until the first divergent edge is reproducible.

**Entry gate:** Complete modules 01.01 and 01.02, gate-00, and the H00 capsule handoff.

**Stage handoff:** A simtrace-v1 edge schema, synthesizable clockwork block, C logic oracle, mutation report, and reset contract.

Use `python3 ftt challenge start ID` to create an evidence workspace. The
checker replays positive and negative commands and verifies every claimed
artifact by hash; it cannot replace the engineering judgment in the rubric.

### Difficulty ladder

- `*` — focused: one main artifact and a narrow adversarial campaign.
- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.
- `***` — boss-scale: integrates the stage and produces the handoff consumed later.

## H01.01 · \* · Faulty LUT Forensic

**Focused · Very Hard · 16–24 hours · archaeology**

**Prerequisites:** 01.01, H00.05, H00.08

Identify swapped inputs, inverted pins, and reversed LUT indexing from sparse black-box samples using minimal probes.

**Artifact:** diagnosis engine, minimal probe set, and repaired LUT map

### Deliverables

- A working diagnosis engine, minimal probe set, and repaired LUT map with reproducible build and invocation instructions.
- An independent model or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with trace hashes, first divergence, invariant, and limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit cycle and memory bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- State changes occur on documented edges and raw traces remain immutable.

### Adversarial campaign

- both inputs swapped
- one pin inverted
- configuration bits reversed

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial schedule replays and the first divergent edge is reported without a crash or hang.
- **A3:** Evidence records seed, tools, hashes, mutation result, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented timing or reset conversion.

**Handoff:** The recovered LUT convention becomes the logic oracle's indexing rule.

**Safety:** All required work is simulation-only; synthesis is optional and does not prove timing closure or electrical behavior.

## H01.02 · \* · LUT ALU Synthesis

**Focused · Brutal · 28–42 hours · construction**

**Prerequisites:** 01.01, H01.01

Construct an eight-bit ALU only from LUT, mux, carry, and register primitives with explicit width and flags.

**Artifact:** structural ALU, exhaustive oracle, and resource report

### Deliverables

- A working structural ALU, exhaustive oracle, and resource report with reproducible build and invocation instructions.
- An independent model or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with trace hashes, first divergence, invariant, and limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit cycle and memory bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- State changes occur on documented edges and raw traces remain immutable.

### Adversarial campaign

- most-significant carry
- signed overflow without carry
- unsupported opcode beside reset

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial schedule replays and the first divergent edge is reported without a crash or hang.
- **A3:** Evidence records seed, tools, hashes, mutation result, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented timing or reset conversion.

**Handoff:** The ALU state schema feeds the clockwork boss and CPU comparisons.

**Safety:** All required work is simulation-only; synthesis is optional and does not prove timing closure or electrical behavior.

## H01.03 · \*\* · Handshake Adversary

**Cumulative · Very Hard · 20–30 hours · adversary**

**Prerequisites:** 01.02, H00.05

Design a ready-valid channel and prove no loss, duplication, or reordering across arbitrary stalls and reset.

**Artifact:** C and RTL channel models, schedule generator, and invariant monitor

### Deliverables

- A working C and RTL channel models, schedule generator, and invariant monitor with reproducible build and invocation instructions.
- An independent model or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with trace hashes, first divergence, invariant, and limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit cycle and memory bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- State changes occur on documented edges and raw traces remain immutable.

### Adversarial campaign

- ready toggling every cycle
- reset with unconsumed item
- completion during consumer stall

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial schedule replays and the first divergent edge is reported without a crash or hang.
- **A3:** Evidence records seed, tools, hashes, mutation result, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented timing or reset conversion.

**Handoff:** The channel contract becomes the MMIO transaction primitive.

**Safety:** All required work is simulation-only; synthesis is optional and does not prove timing closure or electrical behavior.

## H01.04 · \*\* · Sequential Black-Box Inference

**Cumulative · Brutal · 24–36 hours · archaeology**

**Prerequisites:** 01.02, H01.03

Recover hidden reset, enable, rollover, and latency semantics from traces of a sequential component.

**Artifact:** candidate machine family, experiment planner, and final model

### Deliverables

- A working candidate machine family, experiment planner, and final model with reproducible build and invocation instructions.
- An independent model or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with trace hashes, first divergence, invariant, and limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit cycle and memory bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- State changes occur on documented edges and raw traces remain immutable.

### Adversarial campaign

- synchronous versus asynchronous reset
- enable sampled one edge late
- separately registered rollover output

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial schedule replays and the first divergent edge is reported without a crash or hang.
- **A3:** Evidence records seed, tools, hashes, mutation result, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented timing or reset conversion.

**Handoff:** The inference planner is retained for clock, UART, and board archaeology.

**Safety:** All required work is simulation-only; synthesis is optional and does not prove timing closure or electrical behavior.

## H01.05 · \*\* · Waveform Bisection

**Cumulative · Very Hard · 18–27 hours · construction**

**Prerequisites:** 01.02, H01.03

Compare VCD and JSON traces and return the first causally meaningful divergent edge.

**Artifact:** trace normalizer, comparator, and minimized divergence slice

### Deliverables

- A working trace normalizer, comparator, and minimized divergence slice with reproducible build and invocation instructions.
- An independent model or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with trace hashes, first divergence, invariant, and limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit cycle and memory bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- State changes occur on documented edges and raw traces remain immutable.

### Adversarial campaign

- different declaration order
- unknown values before reset
- late visible effect of hidden divergence

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial schedule replays and the first divergent edge is reported without a crash or hang.
- **A3:** Evidence records seed, tools, hashes, mutation result, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented timing or reset conversion.

**Handoff:** simtrace-v1 becomes the shared evidence format.

**Safety:** All required work is simulation-only; synthesis is optional and does not prove timing closure or electrical behavior.

## H01.06 · \*\* · RTL Mutant Killer

**Cumulative · Brutal · 26–39 hours · adversary**

**Prerequisites:** H01.02, H01.03, H01.05

Kill reset, blocking-assignment, stale-state, truncation, and off-by-one RTL mutants.

**Artifact:** mutant suite, discriminating tests, and survivor analysis

### Deliverables

- A working mutant suite, discriminating tests, and survivor analysis with reproducible build and invocation instructions.
- An independent model or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with trace hashes, first divergence, invariant, and limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit cycle and memory bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- State changes occur on documented edges and raw traces remain immutable.

### Adversarial campaign

- reset bug after prior state
- counter width truncation
- output from stale state

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial schedule replays and the first divergent edge is reported without a crash or hang.
- **A3:** Evidence records seed, tools, hashes, mutation result, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented timing or reset conversion.

**Handoff:** The mutation runner and threshold are reused for UART and CPU.

**Safety:** All required work is simulation-only; synthesis is optional and does not prove timing closure or electrical behavior.

## H01.07 · \*\* · C versus RTL Differential

**Cumulative · Brutal · 30–45 hours · integration**

**Prerequisites:** H01.05, H01.06

Compare structurally independent C and synthesizable RTL models edge by edge over generated schedules.

**Artifact:** independent models, differential driver, and mismatch capsules

### Deliverables

- A working independent models, differential driver, and mismatch capsules with reproducible build and invocation instructions.
- An independent model or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with trace hashes, first divergence, invariant, and limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit cycle and memory bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- State changes occur on documented edges and raw traces remain immutable.

### Adversarial campaign

- reset beside input change
- maximum-width rollover
- long stall then transfer

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial schedule replays and the first divergent edge is reported without a crash or hang.
- **A3:** Evidence records seed, tools, hashes, mutation result, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented timing or reset conversion.

**Handoff:** The paired oracle becomes the standard device-validation harness.

**Safety:** All required work is simulation-only; synthesis is optional and does not prove timing closure or electrical behavior.

## H01.08 · \*\*\* · Boss: Deterministic Clockwork

**Boss-Scale · Brutal · 36–54 hours · boss**

**Prerequisites:** H01.02, H01.04, H01.06, H01.07

Compose ALU, inferred FSM, counter, and handshake channel into one reproducible clocked subsystem.

**Artifact:** synthesizable subsystem, C oracle, trace corpus, and seeded mutant

### Deliverables

- A working synthesizable subsystem, C oracle, trace corpus, and seeded mutant with reproducible build and invocation instructions.
- An independent model or property suite plus a seeded adversarial regression corpus.
- A replayable evidence packet with trace hashes, first divergence, invariant, and limitation.

### Constraints

- All required checks run offline with deterministic seeds and explicit cycle and memory bounds.
- Implementation and oracle remain independently replaceable; fixed examples alone are insufficient.
- State changes occur on documented edges and raw traces remain immutable.

### Adversarial campaign

- reset during backpressure
- illegal accepted opcode
- rollover during output transfer

### Acceptance evidence

- **A1:** The artifact builds warning-clean and passes deterministic reference checks from a fresh workspace.
- **A2:** Every adversarial schedule replays and the first divergent edge is reported without a crash or hang.
- **A3:** Evidence records seed, tools, hashes, mutation result, invariant, and known limitation.
- **A4:** A downstream probe consumes the handoff without undocumented timing or reset conversion.

**Handoff:** The frozen simtrace-v1, reset contract, and subsystem pass to bringup.

**Safety:** All required work is simulation-only; synthesis is optional and does not prove timing closure or electrical behavior.

## Primary references

- [Verilator trace options](https://verilator.org/guide/latest/exe_verilator.html#cmdoption-trace) — Produce stable waveform evidence and understand simulator trace controls.
- [AMD configurable logic guide UG574](https://docs.amd.com/r/en-US/ug574-ultrascale-clb) — Relate LUT, carry, register, and control-set models to documented FPGA resources.
- [cocotb timing model](https://docs.cocotb.org/en/stable/timing_model.html) — Define phases, edge observations, and race-free mixed-language checking.
- [Yosys documentation](https://yosyshq.readthedocs.io/projects/yosys/en/latest/) — Inspect synthesized structure while separating logical equivalence from source appearance.

Return to [[Challenge Atlas]].

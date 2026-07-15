---
title: "Hard Track 07 - Evidence-First Physical Bringup"
tags: ["course", "challenge", "hard-track", "stage-07"]
---

# Hard Track 07: Evidence-First Physical Bringup

Reconstruct JTAG and flash protocols, audit board facts, diagnose clocks, and compare C, RTL, and recorded hardware without requiring a live board.

**Entry gate:** Complete modules 07.01 through 07.03 or simulation equivalents, gate-07, and preserve the H06 browser workload.

**Stage handoff:** A reviewed board pack, read-only flash transcript, three-way concordance report, rollback image, and bringup capsule.

Use `python3 ftt challenge start ID` to create an evidence workspace. The
checker replays positive and negative commands and verifies every claimed
artifact by hash; it cannot replace the engineering judgment in the rubric.

### Difficulty ladder

- `*` — focused: one main artifact and a narrow adversarial campaign.
- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.
- `***` — boss-scale: integrates the stage and produces the handoff consumed later.

## H07.01 · \* · TAP from Unknown State

**Focused · Brutal · 28–42 hours · construction**

**Prerequisites:** 07.01, H01.04, H03.05

Model all TAP transitions, recover from any start, and generate shortest paths between every state pair.

**Artifact:** C TAP model, path planner, exhaustive tests, and renderer

### Deliverables

- A working C TAP model, path planner, exhaustive tests, and renderer with reproducible instructions.
- A simulation or recorded-hardware oracle plus seeded fault fixtures.
- A replayable bringup evidence packet with provenance and stop-go decisions.

### Constraints

- Simulation and recorded fixtures satisfy every required acceptance check.
- Board facts, tool facts, protocol hypotheses, and observations remain distinct.
- Live programming or driving is disabled until the reviewed safety gate passes.

### Adversarial campaign

- each of sixteen starts
- five high TMS samples
- pause-to-shift through Exit2

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic simulation and recorded-fixture checks.
- **A2:** Every injected physical-layer hypothesis replays with an earliest owning diagnosis.
- **A3:** Evidence records provenance, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The final capsule consumes prior browser, machine, device, and logic handoffs directly.

**Handoff:** The TAP navigator drives boundary scan and recorded JTAG.

**Safety:** Required work uses simulation and recordings; live work needs an allowlisted board, voltage checks, current limiting, stop rules, and experienced review.

## H07.02 · \* · Boundary-Scan Detective

**Focused · Brutal · 32–48 hours · archaeology**

**Prerequisites:** 07.02, H07.01

Infer swapped, stuck, and open nets from simulated boundary-scan observations using minimal stimuli.

**Artifact:** board-net model, diagnosis engine, planner, and ambiguity report

### Deliverables

- A working board-net model, diagnosis engine, planner, and ambiguity report with reproducible instructions.
- A simulation or recorded-hardware oracle plus seeded fault fixtures.
- A replayable bringup evidence packet with provenance and stop-go decisions.

### Constraints

- Simulation and recorded fixtures satisfy every required acceptance check.
- Board facts, tool facts, protocol hypotheses, and observations remain distinct.
- Live programming or driving is disabled until the reviewed safety gate passes.

### Adversarial campaign

- LED nets swapped
- driven net stuck low
- observation cell disconnected

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic simulation and recorded-fixture checks.
- **A2:** Every injected physical-layer hypothesis replays with an earliest owning diagnosis.
- **A3:** Evidence records provenance, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The final capsule consumes prior browser, machine, device, and logic handoffs directly.

**Handoff:** The diagnosed pin map feeds constraint auditing.

**Safety:** Required work uses simulation and recordings; live work needs an allowlisted board, voltage checks, current limiting, stop rules, and experienced review.

## H07.03 · \*\* · USB-SPI Dialect Archaeology

**Cumulative · Brutal · 34–51 hours · archaeology**

**Prerequisites:** 07.01, H00.01, H02.06

Reconstruct command framing, address order, transfer limits, and errors from realhw-inspired traces without copying branch code.

**Artifact:** protocol specification, mock transport, C client, and corpus

### Deliverables

- A working protocol specification, mock transport, C client, and corpus with reproducible instructions.
- A simulation or recorded-hardware oracle plus seeded fault fixtures.
- A replayable bringup evidence packet with provenance and stop-go decisions.

### Constraints

- Simulation and recorded fixtures satisfy every required acceptance check.
- Board facts, tool facts, protocol hypotheses, and observations remain distinct.
- Live programming or driving is disabled until the reviewed safety gate passes.

### Adversarial campaign

- short USB transfer
- reversed flash address
- all-ones disconnect

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic simulation and recorded-fixture checks.
- **A2:** Every injected physical-layer hypothesis replays with an earliest owning diagnosis.
- **A3:** Evidence records provenance, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The final capsule consumes prior browser, machine, device, and logic handoffs directly.

**Handoff:** The model becomes the read-only flash interface.

**Safety:** Required work uses simulation and recordings; live work needs an allowlisted board, voltage checks, current limiting, stop rules, and experienced review.

## H07.04 · \*\* · Read-Only Flash Forensic

**Cumulative · Brutal · 34–51 hours · adversary**

**Prerequisites:** H07.03

Verify identity and capacity, dump bounded chunks with resume and hashes, and reject disconnect or corruption.

**Artifact:** read-only flash client, mock image, resume manifest, and transcript

### Deliverables

- A working read-only flash client, mock image, resume manifest, and transcript with reproducible instructions.
- A simulation or recorded-hardware oracle plus seeded fault fixtures.
- A replayable bringup evidence packet with provenance and stop-go decisions.

### Constraints

- Simulation and recorded fixtures satisfy every required acceptance check.
- Board facts, tool facts, protocol hypotheses, and observations remain distinct.
- Live programming or driving is disabled until the reviewed safety gate passes.

### Adversarial campaign

- cross-capacity request
- bit flipped on resume
- all-ones identity

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic simulation and recorded-fixture checks.
- **A2:** Every injected physical-layer hypothesis replays with an earliest owning diagnosis.
- **A3:** Evidence records provenance, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The final capsule consumes prior browser, machine, device, and logic handoffs directly.

**Handoff:** The verified image enters the board pack without write authority.

**Safety:** Required work uses simulation and recordings; live work needs an allowlisted board, voltage checks, current limiting, stop rules, and experienced review.

## H07.05 · \*\* · Schematic-to-Constraint Audit

**Cumulative · Brutal · 36–54 hours · archaeology**

**Prerequisites:** 07.02, H00.07

Check board nets against pin, bank-voltage, clock, reset, and I/O constraints with provenance.

**Artifact:** board model, constraint linter, provenance table, and fault fixtures

### Deliverables

- A working board model, constraint linter, provenance table, and fault fixtures with reproducible instructions.
- A simulation or recorded-hardware oracle plus seeded fault fixtures.
- A replayable bringup evidence packet with provenance and stop-go decisions.

### Constraints

- Simulation and recorded fixtures satisfy every required acceptance check.
- Board facts, tool facts, protocol hypotheses, and observations remain distinct.
- Live programming or driving is disabled until the reviewed safety gate passes.

### Adversarial campaign

- two signals on one pin
- wrong bank voltage
- clock missing timing constraint

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic simulation and recorded-fixture checks.
- **A2:** Every injected physical-layer hypothesis replays with an earliest owning diagnosis.
- **A3:** Evidence records provenance, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The final capsule consumes prior browser, machine, device, and logic handoffs directly.

**Handoff:** The reviewed model becomes the optional-live allowlist.

**Safety:** Required work uses simulation and recordings; live work needs an allowlisted board, voltage checks, current limiting, stop rules, and experienced review.

## H07.06 · \*\* · Three-Clocks Bringup

**Cumulative · Brutal · 32–48 hours · archaeology**

**Prerequisites:** 07.03, H02.01, H07.05

Distinguish oscillator, synthesis constraint, and observed timebase while diagnosing reset and pin faults.

**Artifact:** timing ledger, board twin, waveforms, and decision tree

### Deliverables

- A working timing ledger, board twin, waveforms, and decision tree with reproducible instructions.
- A simulation or recorded-hardware oracle plus seeded fault fixtures.
- A replayable bringup evidence packet with provenance and stop-go decisions.

### Constraints

- Simulation and recorded fixtures satisfy every required acceptance check.
- Board facts, tool facts, protocol hypotheses, and observations remain distinct.
- Live programming or driving is disabled until the reviewed safety gate passes.

### Adversarial campaign

- constraint differs from oscillator
- reset releases late
- LED inverted while UART correct

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic simulation and recorded-fixture checks.
- **A2:** Every injected physical-layer hypothesis replays with an earliest owning diagnosis.
- **A3:** Evidence records provenance, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The final capsule consumes prior browser, machine, device, and logic handoffs directly.

**Handoff:** The clock-reset-pin contract aligns all traces.

**Safety:** Required work uses simulation and recordings; live work needs an allowlisted board, voltage checks, current limiting, stop rules, and experienced review.

## H07.07 · \*\* · C-RTL-Board Concordance

**Cumulative · Brutal · 42–63 hours · integration**

**Prerequisites:** 07.03, H01.07, H02.08, H07.06

Align C, RTL, and recorded-board events and locate the first owning mismatch despite capture latency.

**Artifact:** trace aligner, concordance report, replay capsule, and reducer

### Deliverables

- A working trace aligner, concordance report, replay capsule, and reducer with reproducible instructions.
- A simulation or recorded-hardware oracle plus seeded fault fixtures.
- A replayable bringup evidence packet with provenance and stop-go decisions.

### Constraints

- Simulation and recorded fixtures satisfy every required acceptance check.
- Board facts, tool facts, protocol hypotheses, and observations remain distinct.
- Live programming or driving is disabled until the reviewed safety gate passes.

### Adversarial campaign

- one-edge reset offset
- UART capture latency
- correct LED period with wrong phase

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic simulation and recorded-fixture checks.
- **A2:** Every injected physical-layer hypothesis replays with an earliest owning diagnosis.
- **A3:** Evidence records provenance, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The final capsule consumes prior browser, machine, device, and logic handoffs directly.

**Handoff:** The capsule proves which contracts survived hardware translation.

**Safety:** Required work uses simulation and recordings; live work needs an allowlisted board, voltage checks, current limiting, stop rules, and experienced review.

## H07.08 · \*\*\* · Boss: Blind Bringup

**Boss-Scale · Brutal · 72–108 hours · boss**

**Prerequisites:** H06.08, H07.02, H07.04, H07.05, H07.06, H07.07

Stage LED, UART, RAM, boot, and browser bringup with stop-go gates, rollback, and a full boundary ledger.

**Artifact:** reviewed board pack, staged images, rollback, browser transcript, and capsule

### Deliverables

- A working reviewed board pack, staged images, rollback, browser transcript, and capsule with reproducible instructions.
- A simulation or recorded-hardware oracle plus seeded fault fixtures.
- A replayable bringup evidence packet with provenance and stop-go decisions.

### Constraints

- Simulation and recorded fixtures satisfy every required acceptance check.
- Board facts, tool facts, protocol hypotheses, and observations remain distinct.
- Live programming or driving is disabled until the reviewed safety gate passes.

### Adversarial campaign

- wrong LED pin
- UART works but RAM boundary fails
- divergence after packet activation

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic simulation and recorded-fixture checks.
- **A2:** Every injected physical-layer hypothesis replays with an earliest owning diagnosis.
- **A3:** Evidence records provenance, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The final capsule consumes prior browser, machine, device, and logic handoffs directly.

**Handoff:** The final capsule links observations through every course layer.

**Safety:** Required work uses simulation and recordings; live work needs an allowlisted board, voltage checks, current limiting, stop rules, and experienced review.

## Primary references

- [IEEE 1149.1 standard page](https://standards.ieee.org/ieee/1149.1/4484/) — Ground TAP, scan, reset, and boundary-scan terminology in the governing standard.
- [AMD configuration guide UG470](https://docs.amd.com/v/u/en-US/ug470_7Series_Config) — Define configuration, startup, reset, status, and handling for a supported FPGA.
- [Digilent Arty A7 schematic](https://digilent.com/reference/_media/programmable-logic/arty-a7/arty-a7-e2-sch.pdf) — Trace clock, reset, LED, JTAG, power, memory, and connector nets.
- [AMD programming guide UG908](https://docs.amd.com/r/en-US/ug908-vivado-programming-debugging) — Plan staged programming, capture evidence, and rollback with vendor tools.

Return to [[Challenge Atlas]].

---
title: "Hard Track 02 - Bringup Through Hostile Wires"
tags: ["course", "challenge", "hard-track", "stage-02"]
---

# Hard Track 02: Bringup Through Hostile Wires

Treat LED timing, serial framing, MMIO side effects, FIFOs, and host bridges as unknown or adversarial systems.

**Entry gate:** Complete modules 02.01 and 02.02, gate-02, and the H01 clockwork handoff.

**Stage handoff:** A bus-v1 register contract, cycle-accurate UART, recovery console, and transaction corpus.

Use `python3 ftt challenge start ID` to create an evidence workspace. The
checker replays positive and negative commands and verifies every claimed
artifact by hash; it cannot replace the engineering judgment in the rubric.

### Difficulty ladder

- `*` — focused: one main artifact and a narrow adversarial campaign.
- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.
- `***` — boss-scale: integrates the stage and produces the handoff consumed later.

## H02.01 · \* · Unknown-Clock Divider

**Focused · Very Hard · 16–24 hours · archaeology**

**Prerequisites:** 02.01, H01.08

Infer oscillator, divider convention, reset release, and pin inversion from a noisy LED trace.

**Artifact:** clock hypothesis report, divider model, and discriminating tests

### Deliverables

- A working clock hypothesis report, divider model, and discriminating tests with reproducible instructions.
- An independent model plus a seeded adversarial corpus.
- A replayable evidence packet with trace hashes and first divergence.

### Constraints

- Required checks are offline and deterministically bounded.
- Oracle and implementation remain independently replaceable.
- No payload is exposed before its framing or transaction is valid.

### Adversarial campaign

- off-by-one terminal count
- clock wrong by integer factor
- inverted LED pin

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic normal and boundary checks.
- **A2:** Every adversarial case replays as a typed bounded outcome.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared handoff without a hidden adapter.

**Handoff:** The accepted clock-reset contract parameterizes later UART and board traces.

**Safety:** Required transport is mocked or loopback-only; do not attach unknown hardware or drive pins without an electrical plan.

## H02.02 · \* · Autobaud Archaeology

**Focused · Brutal · 22–33 hours · archaeology**

**Prerequisites:** 02.02, H00.04, H01.05

Recover baud, polarity, bit order, and framing from captures with drift, gaps, truncation, and noise.

**Artifact:** capture decoder, hypothesis table, and minimized waveforms

### Deliverables

- A working capture decoder, hypothesis table, and minimized waveforms with reproducible instructions.
- An independent model plus a seeded adversarial corpus.
- A replayable evidence packet with trace hashes and first divergence.

### Constraints

- Required checks are offline and deterministically bounded.
- Oracle and implementation remain independently replaceable.
- No payload is exposed before its framing or transaction is valid.

### Adversarial campaign

- shortened start bit
- reversed polarity
- capture starting mid-frame

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic normal and boundary checks.
- **A2:** Every adversarial case replays as a typed bounded outcome.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared handoff without a hidden adapter.

**Handoff:** The decoded frame schema supplies receiver oracle vectors.

**Safety:** Required transport is mocked or loopback-only; do not attach unknown hardware or drive pins without an electrical plan.

## H02.03 · \*\* · Jittered UART Receiver

**Cumulative · Brutal · 28–42 hours · construction**

**Prerequisites:** H02.02

Implement a cycle-accurate oversampling receiver that emits a byte only after a valid stop bit.

**Artifact:** C and RTL receivers, jitter generator, and error corpus

### Deliverables

- A working C and RTL receivers, jitter generator, and error corpus with reproducible instructions.
- An independent model plus a seeded adversarial corpus.
- A replayable evidence packet with trace hashes and first divergence.

### Constraints

- Required checks are offline and deterministically bounded.
- Oracle and implementation remain independently replaceable.
- No payload is exposed before its framing or transaction is valid.

### Adversarial campaign

- jitter on every bit
- glitch near sample point
- invalid stop after valid data

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic normal and boundary checks.
- **A2:** Every adversarial case replays as a typed bounded outcome.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared handoff without a hidden adapter.

**Handoff:** The receiver becomes the RX half of the bus-v1 UART.

**Safety:** Required transport is mocked or loopback-only; do not attach unknown hardware or drive pins without an electrical plan.

## H02.04 · \*\* · MMIO Register Archaeology

**Cumulative · Brutal · 22–33 hours · archaeology**

**Prerequisites:** 02.02, H00.05, H02.03

Infer ready, overrun, clear-on-read, and write side effects from minimal black-box MMIO probes.

**Artifact:** generated register contract, inference driver, and ambiguity report

### Deliverables

- A working generated register contract, inference driver, and ambiguity report with reproducible instructions.
- An independent model plus a seeded adversarial corpus.
- A replayable evidence packet with trace hashes and first divergence.

### Constraints

- Required checks are offline and deterministically bounded.
- Oracle and implementation remain independently replaceable.
- No payload is exposed before its framing or transaction is valid.

### Adversarial campaign

- status read clearing one flag
- data read while empty
- write as TX becomes full

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic normal and boundary checks.
- **A2:** Every adversarial case replays as a typed bounded outcome.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared handoff without a hidden adapter.

**Handoff:** The machine-readable map becomes the sole UART interface.

**Safety:** Required transport is mocked or loopback-only; do not attach unknown hardware or drive pins without an electrical plan.

## H02.05 · \*\* · FIFO Under Siege

**Cumulative · Brutal · 24–36 hours · adversary**

**Prerequisites:** H01.03, H02.04

Defend bounded TX and RX FIFOs against simultaneous access, backpressure, overflow, and reset.

**Artifact:** C and RTL FIFOs, schedule checker, and invariant log

### Deliverables

- A working C and RTL FIFOs, schedule checker, and invariant log with reproducible instructions.
- An independent model plus a seeded adversarial corpus.
- A replayable evidence packet with trace hashes and first divergence.

### Constraints

- Required checks are offline and deterministically bounded.
- Oracle and implementation remain independently replaceable.
- No payload is exposed before its framing or transaction is valid.

### Adversarial campaign

- enqueue and dequeue while full
- receive overrun
- reset between accept and consume

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic normal and boundary checks.
- **A2:** Every adversarial case replays as a typed bounded outcome.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared handoff without a hidden adapter.

**Handoff:** The verified FIFO completes the UART device model.

**Safety:** Required transport is mocked or loopback-only; do not attach unknown hardware or drive pins without an electrical plan.

## H02.06 · \*\* · Lying Host Bridge

**Cumulative · Very Hard · 20–30 hours · adversary**

**Prerequisites:** H00.03, H02.05

Write a bridge surviving short, delayed, duplicated, and disconnected transfers without inventing data.

**Artifact:** mockable C bridge, typed errors, and deterministic fault script

### Deliverables

- A working mockable C bridge, typed errors, and deterministic fault script with reproducible instructions.
- An independent model plus a seeded adversarial corpus.
- A replayable evidence packet with trace hashes and first divergence.

### Constraints

- Required checks are offline and deterministically bounded.
- Oracle and implementation remain independently replaceable.
- No payload is exposed before its framing or transaction is valid.

### Adversarial campaign

- zero-progress transfer
- all-ones disconnect
- duplicate completion after timeout

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic normal and boundary checks.
- **A2:** Every adversarial case replays as a typed bounded outcome.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared handoff without a hidden adapter.

**Handoff:** The bridge errors feed serial and later USB or network loaders.

**Safety:** Required transport is mocked or loopback-only; do not attach unknown hardware or drive pins without an electrical plan.

## H02.07 · \*\* · UART Mutant Farm

**Cumulative · Brutal · 28–42 hours · adversary**

**Prerequisites:** H02.03, H02.05, H02.06

Differentially test C, RTL, MMIO, and driver layers against timing, status, and retry mutants.

**Artifact:** layered runner, mutant suite, and first-edge capsules

### Deliverables

- A working layered runner, mutant suite, and first-edge capsules with reproducible instructions.
- An independent model plus a seeded adversarial corpus.
- A replayable evidence packet with trace hashes and first divergence.

### Constraints

- Required checks are offline and deterministically bounded.
- Oracle and implementation remain independently replaceable.
- No payload is exposed before its framing or transaction is valid.

### Adversarial campaign

- bit order exchanged
- ready cleared late
- completion before stop bit

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic normal and boundary checks.
- **A2:** Every adversarial case replays as a typed bounded outcome.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared handoff without a hidden adapter.

**Handoff:** The killed-mutant corpus becomes UART conformance evidence.

**Safety:** Required transport is mocked or loopback-only; do not attach unknown hardware or drive pins without an electrical plan.

## H02.08 · \*\*\* · Boss: Recovery Console

**Boss-Scale · Brutal · 38–57 hours · boss**

**Prerequisites:** H02.01, H02.03, H02.04, H02.05, H02.07

Compose a framed console controlling LED and echo while resynchronizing after corruption or reset.

**Artifact:** console protocol, firmware model, UART subsystem, and transcript

### Deliverables

- A working console protocol, firmware model, UART subsystem, and transcript with reproducible instructions.
- An independent model plus a seeded adversarial corpus.
- A replayable evidence packet with trace hashes and first divergence.

### Constraints

- Required checks are offline and deterministically bounded.
- Oracle and implementation remain independently replaceable.
- No payload is exposed before its framing or transaction is valid.

### Adversarial campaign

- flipped length then valid command
- reset mid-response
- backpressure during error report

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic normal and boundary checks.
- **A2:** Every adversarial case replays as a typed bounded outcome.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared handoff without a hidden adapter.

**Handoff:** bus-v1, register map, UART, and recovery transcript pass to processor work.

**Safety:** Required transport is mocked or loopback-only; do not attach unknown hardware or drive pins without an electrical plan.

## Primary references

- [OpenTitan UART theory](https://opentitan.org/book/hw/ip/uart/doc/theory_of_operation.html) — Ground framing, oversampling, FIFOs, interrupts, and errors in a documented UART.
- [OpenTitan UART registers](https://opentitan.org/book/hw/ip/uart/doc/registers.html) — Compare explicit register side effects against the inferred teaching contract.
- [Intel counter HDL guidelines](https://www.intel.com/content/www/us/en/docs/programmable/683082/24-3/counter-hdl-guidelines.html) — Check counter width, enable, reset, and synthesis assumptions used by LED timing.
- [Intel synchronous reset guidance](https://www.intel.com/content/www/us/en/docs/programmable/683082/25-1/use-synchronous-resets.html) — Make reset timing explicit before comparing simulation and observation.

Return to [[Challenge Atlas]].

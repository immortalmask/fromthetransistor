---
title: "Hard Track 04 - Toolchain That Must Survive Itself"
tags: ["course", "challenge", "hard-track", "stage-04"]
---

# Hard Track 04: Toolchain That Must Survive Itself

Drive C0 source through parsing, semantics, ABI, ELF, runtime allocation, packet ownership, and hostile network boot.

**Entry gate:** Complete modules 04.01 through 04.05, gate-04, and the H03 ISA and monitor handoff.

**Stage handoff:** A reproducible C0 toolchain, target ABI, ELF profile, runtime, NIC contract, and boot bundle.

Use `python3 ftt challenge start ID` to create an evidence workspace. The
checker replays positive and negative commands and verifies every claimed
artifact by hash; it cannot replace the engineering judgment in the rubric.

### Difficulty ladder

- `*` — focused: one main artifact and a narrow adversarial campaign.
- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.
- `***` — boss-scale: integrates the stage and produces the handoff consumed later.

## H04.01 · \* · Lexer Minefield

**Focused · Very Hard · 22–33 hours · adversary**

**Prerequisites:** 04.01, H00.06, H03.08

Build a C0 lexer and parser with stable spans that consumes all input or returns one precise error.

**Artifact:** lexer-parser, grammar generator, AST serializer, and diagnostics

### Deliverables

- A working lexer-parser, grammar generator, AST serializer, and diagnostics with reproducible instructions.
- An independent semantic or byte-level oracle plus seeded faults.
- A replayable evidence packet linking source through target effects.

### Constraints

- All builds and transfers are offline, deterministic, and bounded.
- Each layer retains an independent oracle at its declared interface.
- No target image executes before complete range and integrity validation.

### Adversarial campaign

- unterminated nesting
- oversized integer
- valid prefix with ambiguous token

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic source, object, and target checks.
- **A2:** Every adversarial case replays as a precise bounded failure or matching result.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared ABI, image, and device handoff directly.

**Handoff:** The typed AST wire form feeds semantic and code-generation models.

**Safety:** Network tests use packet fixtures or loopback; target images run only in the course machine.

## H04.02 · \* · Semantic Doppelganger

**Focused · Brutal · 38–57 hours · integration**

**Prerequisites:** 04.01, H03.03, H04.01

Compare an AST interpreter with generated target code for thousands of defined C0 programs.

**Artifact:** interpreter, code generator, program generator, and corpus

### Deliverables

- A working interpreter, code generator, program generator, and corpus with reproducible instructions.
- An independent semantic or byte-level oracle plus seeded faults.
- A replayable evidence packet linking source through target effects.

### Constraints

- All builds and transfers are offline, deterministic, and bounded.
- Each layer retains an independent oracle at its declared interface.
- No target image executes before complete range and integrity validation.

### Adversarial campaign

- untaken faulting arm
- target versus host arithmetic
- maximum call depth

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic source, object, and target checks.
- **A2:** Every adversarial case replays as a precise bounded failure or matching result.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared ABI, image, and device handoff directly.

**Handoff:** The proven lowering rules become the compiler contract.

**Safety:** Network tests use packet fixtures or loopback; target images run only in the course machine.

## H04.03 · \*\* · Miscompilation Reducer

**Cumulative · Brutal · 28–42 hours · archaeology**

**Prerequisites:** H04.02

Find the first wrong lowering in compiler mutants and reduce each program while preserving mismatch.

**Artifact:** compiler trace mapper, reducer, and regressions

### Deliverables

- A working compiler trace mapper, reducer, and regressions with reproducible instructions.
- An independent semantic or byte-level oracle plus seeded faults.
- A replayable evidence packet linking source through target effects.

### Constraints

- All builds and transfers are offline, deterministic, and bounded.
- Each layer retains an independent oracle at its declared interface.
- No target image executes before complete range and integrity validation.

### Adversarial campaign

- wrong evaluation order
- spill reloaded at wrong width
- branch fixed before final size

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic source, object, and target checks.
- **A2:** Every adversarial case replays as a precise bounded failure or matching result.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared ABI, image, and device handoff directly.

**Handoff:** Minimal cases enter the permanent compiler corpus.

**Safety:** Network tests use packet fixtures or loopback; target images run only in the course machine.

## H04.04 · \*\* · ABI Ordeal

**Cumulative · Brutal · 30–45 hours · construction**

**Prerequisites:** 00.07, H03.05, H04.02

Prove the target calling convention across separate compilation, recursion, spills, and startup.

**Artifact:** ABI specification, conformance programs, startup object, and checker

### Deliverables

- A working ABI specification, conformance programs, startup object, and checker with reproducible instructions.
- An independent semantic or byte-level oracle plus seeded faults.
- A replayable evidence packet linking source through target effects.

### Constraints

- All builds and transfers are offline, deterministic, and bounded.
- Each layer retains an independent oracle at its declared interface.
- No target image executes before complete range and integrity validation.

### Adversarial campaign

- callee-save pressure
- deep stack alignment
- clobber after nested call

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic source, object, and target checks.
- **A2:** Every adversarial case replays as a precise bounded failure or matching result.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared ABI, image, and device handoff directly.

**Handoff:** The ABI and startup object become linker and kernel inputs.

**Safety:** Network tests use packet fixtures or loopback; target images run only in the course machine.

## H04.05 · \*\* · Linker Labyrinth

**Cumulative · Brutal · 38–57 hours · construction**

**Prerequisites:** 04.02, H00.02, H04.04

Lay out objects, resolve symbols, apply checked relocations, and emit deterministic ELF.

**Artifact:** static linker, ELF inspector, relocation oracle, and malformed corpus

### Deliverables

- A working static linker, ELF inspector, relocation oracle, and malformed corpus with reproducible instructions.
- An independent semantic or byte-level oracle plus seeded faults.
- A replayable evidence packet linking source through target effects.

### Constraints

- All builds and transfers are offline, deterministic, and bounded.
- Each layer retains an independent oracle at its declared interface.
- No target image executes before complete range and integrity validation.

### Adversarial campaign

- duplicate strong symbol
- relocation overflow
- alignment changing relative relocation

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic source, object, and target checks.
- **A2:** Every adversarial case replays as a precise bounded failure or matching result.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared ABI, image, and device handoff directly.

**Handoff:** The ELF profile and map become the OS load contract.

**Safety:** Network tests use packet fixtures or loopback; target images run only in the course machine.

## H04.06 · \*\* · Allocator Chaos

**Cumulative · Brutal · 34–51 hours · adversary**

**Prerequisites:** 04.03, H00.03, H04.04

Implement free-list split, ordered insertion, coalescing, and invariant checks after generated operations.

**Artifact:** allocator, heap oracle, fail schedule, and heap dump

### Deliverables

- A working allocator, heap oracle, fail schedule, and heap dump with reproducible instructions.
- An independent semantic or byte-level oracle plus seeded faults.
- A replayable evidence packet linking source through target effects.

### Constraints

- All builds and transfers are offline, deterministic, and bounded.
- Each layer retains an independent oracle at its declared interface.
- No target image executes before complete range and integrity validation.

### Adversarial campaign

- reverse adjacent frees
- failure after split decision
- alignment exhausting arena

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic source, object, and target checks.
- **A2:** Every adversarial case replays as a precise bounded failure or matching result.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared ABI, image, and device handoff directly.

**Handoff:** Allocator and byte routines form the target runtime.

**Safety:** Network tests use packet fixtures or loopback; target images run only in the course machine.

## H04.07 · \*\* · Treacherous NIC and Loader

**Cumulative · Brutal · 38–57 hours · adversary**

**Prerequisites:** 04.04, 04.05, H02.05, H04.05, H04.06

Compose MMIO packet rings with a loader surviving loss, duplication, reordering, and truncation.

**Artifact:** NIC model, driver, image protocol, loader, and transcript

### Deliverables

- A working NIC model, driver, image protocol, loader, and transcript with reproducible instructions.
- An independent semantic or byte-level oracle plus seeded faults.
- A replayable evidence packet linking source through target effects.

### Constraints

- All builds and transfers are offline, deterministic, and bounded.
- Each layer retains an independent oracle at its declared interface.
- No target image executes before complete range and integrity validation.

### Adversarial campaign

- ownership changes during retry
- duplicate final packet
- checksum with overlapping range

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic source, object, and target checks.
- **A2:** Every adversarial case replays as a precise bounded failure or matching result.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared ABI, image, and device handoff directly.

**Handoff:** NIC and boot-bundle contracts become kernel inputs.

**Safety:** Network tests use packet fixtures or loopback; target images run only in the course machine.

## H04.08 · \*\*\* · Boss: Source to Packet Boot

**Boss-Scale · Brutal · 50–75 hours · boss**

**Prerequisites:** H04.03, H04.04, H04.05, H04.06, H04.07

Compile multi-file C0, link, package, transfer through the faulting NIC, boot, and emit UART proof.

**Artifact:** reproducible toolchain, boot bundle, runner, and boundary ledger

### Deliverables

- A working reproducible toolchain, boot bundle, runner, and boundary ledger with reproducible instructions.
- An independent semantic or byte-level oracle plus seeded faults.
- A replayable evidence packet linking source through target effects.

### Constraints

- All builds and transfers are offline, deterministic, and bounded.
- Each layer retains an independent oracle at its declared interface.
- No target image executes before complete range and integrity validation.

### Adversarial campaign

- compiler mutant visible on target
- reordered transfer packet
- allocator exhaustion during output

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic source, object, and target checks.
- **A2:** Every adversarial case replays as a precise bounded failure or matching result.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared ABI, image, and device handoff directly.

**Handoff:** Toolchain, ABI, runtime, bundle, and NIC trace pass to kernel work.

**Safety:** Network tests use packet fixtures or loopback; target images run only in the course machine.

## Primary references

- [LLVM frontend tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/) — Structure lexing, parsing, ASTs, code generation, and staged language growth.
- [System V ABI ELF PDF](https://gabi.xinuos.com/elf.pdf) — Define sections, symbols, relocations, segments, and loading evidence.
- [Linux DMA mapping guide](https://docs.kernel.org/core-api/dma-api-howto.html) — Ground packet-buffer ownership and device visibility transitions.
- [RFC 1350 TFTP](https://www.rfc-editor.org/rfc/rfc1350.html) — Study a small transfer protocol's blocks, timeouts, duplicates, and errors.

Return to [[Challenge Atlas]].

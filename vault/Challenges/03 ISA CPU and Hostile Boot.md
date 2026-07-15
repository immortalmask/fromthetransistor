---
title: "Hard Track 03 - ISA CPU and Hostile Boot"
tags: ["course", "challenge", "hard-track", "stage-03"]
---

# Hard Track 03: ISA CPU and Hostile Boot

Reconstruct instruction encodings, build independent execution models, mutate them, and carry an unknown ROM through hostile serial boot.

**Entry gate:** Complete modules 03.01 through 03.03, gate-03, and the H02 recovery-console handoff.

**Stage handoff:** A versioned ISA, assembler corpus, CPU trace ABI, boot monitor, and independently checked ROM repair.

Use `python3 ftt challenge start ID` to create an evidence workspace. The
checker replays positive and negative commands and verifies every claimed
artifact by hash; it cannot replace the engineering judgment in the rubric.

### Difficulty ladder

- `*` — focused: one main artifact and a narrow adversarial campaign.
- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.
- `***` — boss-scale: integrates the stage and produces the handoff consumed later.

## H03.01 · \* · ISA Archaeology

**Focused · Brutal · 26–39 hours · archaeology**

**Prerequisites:** 03.01, H00.01, H02.08

Infer opcode fields, signed immediates, reserved encodings, and control flow from binaries and traces.

**Artifact:** recovered ISA table, probe programs, and confidence ledger

### Deliverables

- A working recovered ISA table, probe programs, and confidence ledger with reproducible instructions.
- An independently structured oracle and seeded conformance corpus.
- A replayable evidence packet with hashes and minimized divergence.

### Constraints

- All execution has explicit instruction, memory, and input budgets.
- Oracle and implementation share only the versioned architecture contract.
- Unsupported encodings and programs fail closed inside emulation.

### Adversarial campaign

- opcodes differing in reserved nibble
- negative branch crossing zero
- state change without output

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic architecture checks.
- **A2:** Every adversarial program replays with precise committed state or fault.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared image and trace handoff directly.

**Handoff:** The recovered table becomes isa-v1.

**Safety:** Unknown target programs execute only inside bounded course emulators or an isolated comparison oracle.

## H03.02 · \* · Lossless Assembler and Disassembler

**Focused · Brutal · 30–45 hours · construction**

**Prerequisites:** 03.01, H03.01

Implement labels, canonical disassembly, and rejection classes for the entire frozen FTT-16 word space.

**Artifact:** assembler, disassembler, word classifier, and diagnostic corpus

### Deliverables

- A working assembler, disassembler, word classifier, and diagnostic corpus with reproducible instructions.
- An independently structured oracle and seeded conformance corpus.
- A replayable evidence packet with hashes and minimized divergence.

### Constraints

- All execution has explicit instruction, memory, and input budgets.
- Oracle and implementation share only the versioned architecture contract.
- Unsupported encodings and programs fail closed inside emulation.

### Adversarial campaign

- every valid word
- reserved bits on valid opcode
- branch limits

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic architecture checks.
- **A2:** Every adversarial program replays with precise committed state or fault.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared image and trace handoff directly.

**Handoff:** The conformance corpus feeds CPU and compiler tests.

**Safety:** Unknown target programs execute only inside bounded course emulators or an isolated comparison oracle.

## H03.03 · \*\* · Independent CPU Oracle

**Cumulative · Brutal · 36–54 hours · integration**

**Prerequisites:** 03.02, H03.02

Compare a C executor with a structurally independent state oracle after every instruction.

**Artifact:** two CPU models, program generator, and fault corpus

### Deliverables

- A working two CPU models, program generator, and fault corpus with reproducible instructions.
- An independently structured oracle and seeded conformance corpus.
- A replayable evidence packet with hashes and minimized divergence.

### Constraints

- All execution has explicit instruction, memory, and input budgets.
- Oracle and implementation share only the versioned architecture contract.
- Unsupported encodings and programs fail closed inside emulation.

### Adversarial campaign

- out-of-range branch before write
- byte arithmetic wrap
- bad encoding after legal store

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic architecture checks.
- **A2:** Every adversarial program replays with precise committed state or fault.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared image and trace handoff directly.

**Handoff:** The CPU trace ABI becomes the target execution oracle.

**Safety:** Unknown target programs execute only inside bounded course emulators or an isolated comparison oracle.

## H03.04 · \*\* · CPU Mutant Tournament

**Cumulative · Brutal · 30–45 hours · adversary**

**Prerequisites:** H03.03

Kill ALU, sign-extension, PC, bounds, decode, and partial-commit mutants with minimized programs.

**Artifact:** mutation suite, minimized programs, and survivor analysis

### Deliverables

- A working mutation suite, minimized programs, and survivor analysis with reproducible instructions.
- An independently structured oracle and seeded conformance corpus.
- A replayable evidence packet with hashes and minimized divergence.

### Constraints

- All execution has explicit instruction, memory, and input budgets.
- Oracle and implementation share only the versioned architecture contract.
- Unsupported encodings and programs fail closed inside emulation.

### Adversarial campaign

- zero-extended branch
- PC advanced after halt
- write before memory fault

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic architecture checks.
- **A2:** Every adversarial program replays with precise committed state or fault.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared image and trace handoff directly.

**Handoff:** The corpus becomes architectural regression evidence.

**Safety:** Unknown target programs execute only inside bounded course emulators or an isolated comparison oracle.

## H03.05 · \*\* · Reverse-Time Debugger

**Cumulative · Brutal · 32–48 hours · construction**

**Prerequisites:** 03.02, H03.03

Implement checkpoints, reverse-step, watchpoint search, and first-divergence navigation.

**Artifact:** reversible debugger, checkpoint format, and query transcript

### Deliverables

- A working reversible debugger, checkpoint format, and query transcript with reproducible instructions.
- An independently structured oracle and seeded conformance corpus.
- A replayable evidence packet with hashes and minimized divergence.

### Constraints

- All execution has explicit instruction, memory, and input budgets.
- Oracle and implementation share only the versioned architecture contract.
- Unsupported encodings and programs fail closed inside emulation.

### Adversarial campaign

- reverse across store
- search repeated loop states
- fault with no committed writes

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic architecture checks.
- **A2:** Every adversarial program replays with precise committed state or fault.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared image and trace handoff directly.

**Handoff:** The debugger is reused for compiler and kernel divergence.

**Safety:** Unknown target programs execute only inside bounded course emulators or an isolated comparison oracle.

## H03.06 · \*\* · Architecture Compatibility Island

**Cumulative · Brutal · 44–66 hours · construction**

**Prerequisites:** 03.02, H03.03

Implement a bounded ARMv4T A32 or approved RV32I subset behind the same trace ABI and compare an independent emulator.

**Artifact:** subset specification, executor, cross-assembled fixtures, and differential report

### Deliverables

- A working subset specification, executor, cross-assembled fixtures, and differential report with reproducible instructions.
- An independently structured oracle and seeded conformance corpus.
- A replayable evidence packet with hashes and minimized divergence.

### Constraints

- All execution has explicit instruction, memory, and input budgets.
- Oracle and implementation share only the versioned architecture contract.
- Unsupported encodings and programs fail closed inside emulation.

### Adversarial campaign

- condition-code boundary
- unsupported alignment
- valid instruction outside subset

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic architecture checks.
- **A2:** Every adversarial program replays with precise committed state or fault.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared image and trace handoff directly.

**Handoff:** The adapter proves later interfaces are architecture contracts.

**Safety:** Unknown target programs execute only inside bounded course emulators or an isolated comparison oracle.

## H03.07 · \*\* · Hostile ROM Monitor

**Cumulative · Brutal · 30–45 hours · adversary**

**Prerequisites:** 03.03, H02.08, H03.03

Implement a range-checked checksummed monitor recovering from arbitrary serial byte loss.

**Artifact:** monitor image, host sender, split corpus, and boot transcript

### Deliverables

- A working monitor image, host sender, split corpus, and boot transcript with reproducible instructions.
- An independently structured oracle and seeded conformance corpus.
- A replayable evidence packet with hashes and minimized divergence.

### Constraints

- All execution has explicit instruction, memory, and input budgets.
- Oracle and implementation share only the versioned architecture contract.
- Unsupported encodings and programs fail closed inside emulation.

### Adversarial campaign

- dropped byte in each position
- valid checksum with bad destination
- reset before jump

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic architecture checks.
- **A2:** Every adversarial program replays with precise committed state or fault.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared image and trace handoff directly.

**Handoff:** The monitor becomes the trusted later boot transport.

**Safety:** Unknown target programs execute only inside bounded course emulators or an isolated comparison oracle.

## H03.08 · \*\*\* · Boss: Mystery Cartridge

**Boss-Scale · Brutal · 42–63 hours · boss**

**Prerequisites:** H03.04, H03.05, H03.07

Reverse an unknown ROM, diagnose its logic flaw, patch it, upload through the monitor, and prove the repair.

**Artifact:** annotated ROM, patch, uploaded image, and before-after trace

### Deliverables

- A working annotated ROM, patch, uploaded image, and before-after trace with reproducible instructions.
- An independently structured oracle and seeded conformance corpus.
- A replayable evidence packet with hashes and minimized divergence.

### Constraints

- All execution has explicit instruction, memory, and input budgets.
- Oracle and implementation share only the versioned architecture contract.
- Unsupported encodings and programs fail closed inside emulation.

### Adversarial campaign

- misleading dead code
- data resembling instructions
- late symptom of wrong branch

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic architecture checks.
- **A2:** Every adversarial program replays with precise committed state or fault.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared image and trace handoff directly.

**Handoff:** The repaired image, isa-v1, debugger, and corpus pass to the compiler stage.

**Safety:** Unknown target programs execute only inside bounded course emulators or an isolated comparison oracle.

## Primary references

- [RISC-V RV32I specification](https://docs.riscv.org/reference/isa/unpriv/rv32.html) — Compare a production fixed-width ISA's encoding, state, and exception language with FTT-16.
- [GNU assembler manual](https://sourceware.org/binutils/docs/as/) — Study mature syntax, diagnostics, symbols, and sections while keeping the course format bounded.
- [MCUboot serial recovery](https://docs.mcuboot.com/serial_recovery.html) — Inform framing, resynchronization, validation, and explicit recovery boundaries.
- [Sail RISC-V formal model](https://github.com/riscv/sail-riscv) — Use an independently structured executable specification as a differential-testing model.

Return to [[Challenge Atlas]].

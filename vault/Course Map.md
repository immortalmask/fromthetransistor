---
title: "Course Map"
tags: ["course", "map", "moc"]
---

# Course Map

The original syllabus asks one cumulative question: how much of the modern computer stack can you explain because you built the layer below it? This course keeps that intent and turns it into a runnable path with narrow interfaces, deterministic tests, and explicit exit artifacts.

## Sections

| Section | Expected pace | Cumulative result |
|---|---:|---|
| [[00 C Runway/index|00 C Runway]] | 3 weeks | You can inspect bytes, reason about C memory, read an ABI trace, and model a state machine. |
| [[01 Intro/index|01 Intro]] | 1 week | You can connect switches, gates, LUTs, RTL, simulation, assertions, and waveforms. |
| [[02 Bringup/index|02 Bringup]] | 2 weeks | The simulated machine has timed state, an LED, and a documented UART/MMIO console. |
| [[03 Processor/index|03 Processor]] | 6 weeks | Assembly becomes bytes, a CPU executes them, and a ROM monitor loads programs safely. |
| [[04 Compiler/index|04 Compiler]] | 8 weeks | A bounded C toolchain and runtime can build a network-loaded target program. |
| [[05 Operating System/index|05 Operating System]] | 10 weeks | Protected processes, syscalls, storage, FAT, init, shell, and utilities run together. |
| [[06 Browser/index|06 Browser]] | 6 weeks | The machine speaks scoped TCP and renders a local HTTP/HTML page in a terminal. |
| [[07 Physical/index|07 Physical]] | 6–10 weeks, optional | The proven simulated design is carried to supported FPGA hardware in controlled stages. |

At 12–15 focused hours per week, the required path is about 36 weeks. The physical section and dynamic linking are optional. The old 12-week estimate is useful as a statement of ambition, not as a safe plan for a learner who is also learning C.

Every module links a small English source set to its actual workbook and
homework decisions. Use [[Reference Shelf]] as an index; it is intentionally
organized by this dependency map rather than as a separate reading curriculum.

## Dependency spine

```text
C, bytes, ABI, digital logic
  -> simulation -> LED -> UART/MMIO
  -> ISA + assembler -> CPU -> ROM monitor
  -> C compiler -> ELF linker -> freestanding runtime
  -> packet device -> network boot
  -> MMU -> kernel -> block device -> FAT -> userland
  -> ARP/IP/TCP -> terminal browser
  -> optional dynamic linker
  -> optional JTAG, FPGA board, and physical bringup
```

The assembler and processor can be studied together only after the instruction encodings are frozen. The compiler can begin after the ABI is written down. Required modules never depend on an optional module.

[[Notebook Guide]] turns this dependency spine into five executable analyses.
Each level consumes checked evidence from earlier levels, so later integration
cannot silently replace the byte, framing, machine-image, or system contracts.

## Advanced depth track

The normal modules teach and scaffold the interfaces. [[Challenge Atlas]] is a
separate 64-problem gauntlet for learners who want whole-system depth closer to
the scale suggested by the historical outline. Every stage contains eight
problems across archaeology, construction, adversarial testing, integration,
and a boss. The boss artifact is retained as input to the next stage.

Within each stage, `*` marks focused entry problems, `**` marks cumulative or
adversarial work, and `***` marks the boss. Stars measure integration scope;
even a one-star hard-track problem assumes the corresponding core gate.

Do any six of the seven non-boss stage problems plus its boss for stage mastery;
do all eight for the black track. Passing the evidence runner proves the packet is
hashed and replayable, not that an open-ended design has been exhaustively
proven. The measured rationale and remaining fixture gap are in
[[Depth Audit and Geohot Alignment]].

## Coherent software-first adaptations

The source outline remains preserved in `course/source-outline.json`, including its **ARM7 CPU** and **Haskell C compiler** wording. The executable path makes three deliberate adaptations:

1. **FTT-16 teaching ISA instead of a complete ARM7.** ARM7TDMI does not provide the MMU assumed by the later “ARM9ish” section, and a compatible pipelined ARM core would dominate the course. FTT-16 uses eight fixed-width operations, sixteen 8-bit registers, separate bounded instruction/data spaces, and explicit failure budgets. That is enough to make encoding, control flow, memory effects, and differential traces concrete. Later MMU and OS modules extend the conceptual machine behind explicit interfaces instead of claiming binary compatibility. ARM decoding and an open production ISA such as RISC-V remain valuable comparative extensions.
2. **Python compiler implementation instead of required Haskell.** Python is already needed for the assembler and reference models. It keeps attention on parsing, types, lowering, ABI, and generated code. A Haskell implementation can be added as a comparative functional-programming track; it is not required to learn C systems programming.
3. **Behavioral devices before physical devices.** UART remains the detailed RTL peripheral. Ethernet and storage first use deterministic packet and disk-image backends. Their MMIO and driver boundaries remain real; electrical timing, TAP access, PHYs, SD signaling, and PCB assembly move to optional extensions.

The processor block starts with a cycle- or instruction-accurate emulator because inspectable architectural state is the best oracle. A synthesizable single-cycle RTL implementation can then be checked against it. Pipelining is a stretch exercise after correctness, not the first implementation.

## Completion gates

- **gate-00:** debug a C/byte representation fault and explain the object bounds involved.
- **gate-02:** interpret a waveform and repair a UART or MMIO boundary error.
- **gate-03:** decode bytes, follow a trace, and diagnose a processor/boot divergence.
- **gate-04:** follow a value through compiler, relocation, startup, and allocator behavior.
- **gate-05:** investigate a page fault, syscall, process transition, and filesystem artifact.
- **gate-06:** trace a request through packets, TCP state, HTTP parsing, and terminal output.
- **gate-07:** optional physical fault isolation and bringup evidence.

Each gate combines an automatically graded question bank with a separate practical investigation. A score cannot replace the practical artifact.

## What “browser complete” means

The capstone browser is intentionally bounded: local deterministic service, numeric address or minimal DNS fixture, HTTP without TLS, a small HTML tokenizer/tree, text layout, ANSI rendering, links, and history. CSS, JavaScript, images, cookies, certificates, and production Internet compatibility are outside the core. The browser must have a static-link path, so optional dynamic linking cannot block it.

[[Capstone - Browser in a Box|Browser in a Box]] defines the final linked trace,
fault campaign, reproducibility evidence, and a stretch ladder that moves pieces
onto the course machine without breaking the last known-good host version.

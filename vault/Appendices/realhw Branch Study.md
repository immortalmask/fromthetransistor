---
id: "appendix-realhw-branch-study"
title: "realhw Branch Study"
section: "appendices"
tags: ["course", "real-hardware", "provenance", "bringup", "integration"]
---

# `realhw` Branch Study

## Why study it

George Hotz's [`realhw` branch](https://github.com/geohot/fromthetransistor/tree/9ef169c4828d432db099cea5a76c24a4af4f526c)
is a useful historical trace of the original course idea becoming physical. The
2018 snapshot contains the broad transistor-to-browser outline, board and tool
notes, a partial Spartan-6 LX9 LED synthesis attempt, and exploratory USB/SPI
flash access. It is not a completed first section or a current reference
implementation. There is no license file in that branch, so this course cites
and analyzes it without copying its code.

The valuable pattern is its vertical ambition: a visible LED is connected to
configuration storage, JTAG, the future CPU, and eventually the software stack.
The weakness is equally educational: exploratory code and a successful-looking
demo do not yet provide portable contracts, deterministic tests, provenance, or
a safe bring-up ladder.

## Evidence inventory

| Historical artifact | Direct observation | Missing evidence to reconstruct |
|---|---|---|
| `section2/blink/ledflash.v` | A board-specific counter drives four LED bits through Spartan-6 clock primitives. | Reset behavior, initialized state, exact period, constraints, simulation oracle, synthesis report, and board observation. |
| XST/map scripts | The experiment selected a Spartan-6 part and began a vendor-specific implementation flow. | Complete synthesis-to-bitstream commands, tool versions, constraint provenance, return-code checks, artifact hashes, and timing results. |
| `section2/flasher/spi.py` | USB bulk commands were inferred well enough to issue SPI transfers. | Protocol specification, endianness tests, short-transfer handling, disconnect/timeout states, mock transport, and ownership cleanup. |
| `section2/flasher/dump.py` | The intended workflow read an SPI flash in fixed-size chunks. | JEDEC identity verification, capacity/bounds checks, partial-read recovery, output checksum, immutable destination policy, and comparison with a known image. |
| Datasheet pointers and notes | Board, flash, configuration, I/O, and clock documentation were being collected. | Exact document revisions, requirements extracted per decision, and a trace from each schematic net or register field to a test. |

## Cumulative reconstruction ladder

Do not reproduce the branch as one hardware leap. Reconstruct its observable
contracts using the knowledge spine of this course:

1. **Bytes and C — section 00.** Decode a synthetic JEDEC-ID response and
   address bytes with fixed-width unsigned operations. Reject truncation,
   overflow, impossible capacity, and host-endian reinterpretation.
2. **Logic and time — sections 01–02.** Express the LED counter as old state,
   inputs, next state, and outputs. Derive its period, define reset, test every
   boundary cycle, and compare an optional RTL trace with the C oracle.
3. **Machine and toolchain — sections 03–04.** Treat the configuration image as
   a bounded binary format with explicit load address, length, and checksum.
   Inspect compiler/linker output before bytes become boot input.
4. **Protection and storage — section 05.** Reuse checked ranges, block-device
   fault injection, and FAT-style sector discipline when modeling flash reads.
   A dump command must never imply permission to touch an arbitrary host device.
5. **Protocols and presentation — section 06.** Carry transport failures as
   typed results rather than all-zero data. Render a concise diagnostic report
   through the same bounded text pipeline used by the browser.
6. **Physical evidence — section 07.** Only after the transcript passes in
   simulation, map JTAG/SPI/clock/reset signals to a supported board, verify
   voltage and ownership, limit clock rate, and compare captured hardware events
   with the frozen expected transcript.

Each stage consumes a tested artifact from the previous stage. A hardware
observation may confirm the composition, but it cannot replace the earlier
contracts.

## Workbook investigation

Create a synthetic 64-byte SPI flash and a mock USB transport. Record every
command and response. Then introduce, one at a time:

- a reversed three-byte address;
- a short USB bulk read;
- an all-ones disconnected-target response;
- a request that crosses the declared flash capacity;
- a single flipped bit in the returned chunk;
- a reset that releases one clock later than the model expects.

For each fault, identify the earliest layer that can detect it, the typed error
that must cross the next interface, and the regression test that prevents a
later browser or filesystem symptom from hiding the cause.

## Depth questions

1. Which parts of the branch are board facts, vendor-tool facts, protocol
   hypotheses, and author intent?
2. What evidence would distinguish a wrong LED period from an incorrect clock
   constraint or a pin-mapping error?
3. Why must an SPI flash reader verify identity and capacity before a bulk dump?
4. Which properties can a C model prove exhaustively, which require RTL
   simulation, and which remain electrical measurements?
5. How would you preserve one failing hardware transcript so it can be replayed
   without the board?

## Expansion beyond the historical snapshot

The active course deliberately adds a C runway, strict lab compilation,
malformed-input and boundary tests, model-versus-implementation comparison,
fault injection, a stable teaching ISA, a checked toolchain, an operating-system
and browser integration path, and a supported-board-first safety policy. Use
the branch for questions and provenance—not as a shortcut around those layers.

Continue with [[02.01 Blinking an LED]], [[07.01 JTAG Interface]],
[[07.02 FPGA Board]], [[07.03 Hardware Bringup]], and [[Scope Decisions]].

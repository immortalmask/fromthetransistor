---
title: "03 Processor"
section: "03"
tags: ["course", "moc", "processor"]
---

# 03 Processor

This section turns an ISA table into a complete causal chain: source assembly becomes encoded bytes, architectural state changes one instruction at a time, and a small trusted ROM loads new programs over the console.

## Modules

1. [[03.01 Assembler and ISA]] — encodings, labels, immediates, diagnostics, and ABI assumptions.
2. [[03.02 CPU Emulator]] — fetch/decode/execute, bounded memory, traps, traces, and optional RTL differential testing.
3. [[03.03 Boot ROM Monitor]] — resynchronizing serial protocol, checked RAM writes, checksums, and safe transfer of control.

## Section artifact

One command assembles a program, loads it through the ROM monitor, executes it in the CPU model, and captures deterministic UART plus instruction-trace evidence. Pass `gate-03` before treating the processor as a trusted compiler or kernel target.

Return to [[Course Map]].

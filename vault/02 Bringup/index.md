---
title: "02 Bringup"
section: "02"
tags: ["course", "moc", "bringup"]
---

# 02 Bringup

The simulated computer first becomes observable through a timed output, then communicative through a serial device and MMIO contract.

## Modules

1. [[02.01 Blinking an LED]] — counter width, reset, timing arithmetic, and boundary-cycle assertions.
2. [[02.02 UART and MMIO]] — framed serial state machines, queues, register side effects, and error recovery.

## Section artifact

A self-checking UART/MMIO subsystem that echoes bytes, controls the LED, detects malformed input, and produces a short annotated waveform. Pass `gate-02` before integrating the console with the CPU.

Return to [[Course Map]].

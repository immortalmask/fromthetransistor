---
id: "gate-02"
title: "Synchronous Bringup Gate"
section: "exams"
tags: ["exam", "uart", "mmio", "waveforms"]
---

# Synchronous Bringup Gate

## Purpose

This gate tests cycle-level reasoning about registers, reset, UART framing, and MMIO side effects. A visibly blinking LED is not sufficient evidence; the result must be predictable at boundary cycles.

## Objective knowledge

Run `python3 ftt exam gate-02` and answer without a simulator first. Grade using the printed command, then attach a one-sentence counterexample for each incorrect alternative you chose.

## Practical investigation

A UART echo design passes ordinary text but intermittently duplicates a byte when software reads the data register as a new frame completes. You receive RTL or a software mirror, a short waveform, and an MMIO access trace.

Produce a cycle table containing reset, RX state, sample counter, shift register, ready flag, bus read, and returned byte. Mark the first cycle where expected and actual state differ. Decide whether the root cause is sampling, nonblocking-update timing, read-to-clear semantics, or uncoordinated ownership; prove the choice with a one-change experiment.

Repair the design and add tests for reset during a frame, bad stop bit, back-to-back frames, read on completion cycle, unread-data overrun, and baud-divider boundary. The check must use bounded simulated cycles rather than human-visible timing.

## Rubric

- 25% correct pre-run cycle and frame prediction.
- 25% first-divergence localization supported by waveform and MMIO evidence.
- 25% repair preserving documented register side effects.
- 15% adversarial boundary tests and deterministic replay.
- 10% explanation of the state/ownership invariant that was violated.

## Safety and limits

Simulation is the required environment. Physical serial adapters are optional; if used, verify voltage levels and common ground. Never connect an unknown-voltage UART directly to a board.

## Completion evidence

Submit the objective score, annotated waveform, cycle table, minimal failing test, fixed trace, and register-contract update if behavior changed.

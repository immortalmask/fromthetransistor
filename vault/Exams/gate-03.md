---
id: "gate-03"
title: "Processor and Boot Gate"
section: "exams"
tags: ["exam", "assembler", "cpu", "boot"]
---

# Processor and Boot Gate

## Purpose

This gate checks that instruction bytes, architectural state, and the boot protocol form one coherent contract. You must diagnose the first wrong state, not merely report that a program printed the wrong value.

## Objective knowledge

Run `python3 ftt exam gate-03`, answer from the ISA and boot specifications, and grade with the command shown. For each miss, locate the relevant field or invariant in your own notes.

## Practical investigation

A short assembled program works until a forward conditional branch crosses a label. The emulator then fetches an invalid instruction after upload through the boot monitor. You receive source, symbol table, emitted words, upload transcript, and architectural traces from the learner model and reference model.

Before running anything, calculate label byte addresses, branch displacement, encoded immediate fields, upload destination range, and checksum. Compare traces register by register and identify the first divergent PC or state write. Determine independently whether the assembler, loader, fetch/decode, or execute stage is at fault.

Repair the responsible layer and add one backward branch, boundary-fit displacement, overflow rejection, misaligned fetch, corrupt upload, and protected-range test. Preserve the original failure as a regression fixture.

## Rubric

- 25% correct hand encoding, addresses, and boot-range prediction.
- 25% first architectural divergence localized to one component.
- 25% repair plus encoding/range boundary tests.
- 15% deterministic differential trace and minimized reproducer.
- 10% explanation of the ISA or boot invariant that prevents recurrence.

## Safety and limits

Execute only in the course emulator or optional isolated QEMU oracle. Never jump from the host into uploaded bytes, and never accept a checksum as a substitute for address validation.

## Completion evidence

Keep the objective score, encoding worksheet, before/after binary bytes, first-divergence trace, minimized source, and passing regression results.

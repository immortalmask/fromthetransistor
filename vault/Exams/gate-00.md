---
id: "gate-00"
title: "C and Machine Foundations Gate"
section: "exams"
tags: ["exam", "c", "foundations", "debugging"]
---

# C and Machine Foundations Gate

## Purpose

This gate checks whether you can reason about C objects, bytes, bounds, ownership, calls, and state transitions before those ideas are embedded in larger systems. The catalog owns the passing threshold.

## Objective knowledge

Run `python3 ftt exam gate-00`, record your answers before requesting explanations, then grade with the command it prints. For every miss, write why your selected answer fails on a concrete input.

## Practical investigation

You receive a small C packet decoder, one valid fixture, one truncated fixture, a compiler warning transcript, and a sanitizer report. The valid fixture prints the wrong 16-bit value on one host; the truncated fixture performs an out-of-bounds read.

Before editing:

1. Draw the input object and mark every byte the decoder may read.
2. Predict the decoded value under little- and big-endian host assumptions.
3. Identify the first expression whose precondition is unproven.
4. State ownership and lifetime for the input, decoded record, and output buffer.

Repair the decoder using explicit byte operations and checked lengths. Add tests for zero length, exact minimum length, one-byte truncation, maximum field values, and a deliberately misaligned input address. Submit the before/after trace and explain one invariant that rules out recurrence.

## Rubric

- 25% accurate object, byte, and control-flow predictions before execution.
- 25% localization of the first invalid read or representation assumption.
- 25% portable repair with warning-clean, boundary-focused tests.
- 15% ownership, lifetime, and bounds invariant explained in plain language.
- 10% concise evidence: command, input, expected result, actual result, conclusion.

## Safety and limits

Use only the supplied fixtures and learner workspace. Do not feed unknown native binaries to the host, disable compiler diagnostics, or “fix” the failure with packed casts or unchecked pointer arithmetic.

## Completion evidence

Keep the objective score, prediction sheet, minimized failing input, patch, test output, and a short note naming the earliest false assumption.

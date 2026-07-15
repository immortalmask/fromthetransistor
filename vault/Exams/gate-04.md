---
id: "gate-04"
title: "Compiler and Runtime Gate"
section: "exams"
tags: ["exam", "compiler", "linker", "runtime"]
---

# Compiler and Runtime Gate

## Purpose

This gate checks whether you can follow one value from C source through compiler stages, linked addresses, runtime memory, and an image handoff while maintaining explicit bounds and ownership.

## Objective knowledge

Run `python3 ftt exam gate-04`, commit to all five answers, and grade using the printed command. Correct any miss by tracing a concrete example through the relevant representation.

## Practical investigation

A two-object C0 program links and boots but corrupts the allocator after its second function call. Provided evidence includes tokens and AST, generated assembly, symbol/relocation tables, link map, heap dumps, and bootloader placement trace.

Predict the call frame, relocated addresses, allocation sizes, and free-list state before execution. Find the earliest artifact that contradicts that prediction. Your report must distinguish among wrong code generation, relocation arithmetic, stack alignment, allocator split/coalesce, and image overlap.

Make the smallest correct repair. Add a cross-object call, maximum relocation, undersized split remainder, double free, image overlap, and reordered-chunk regression. Explain why downstream symptoms disappear without adding special cases there.

## Rubric

- 20% accurate source-to-address and heap-state predictions.
- 30% first incorrect representation identified with evidence.
- 25% repair and focused boundary/failure tests.
- 15% compiler, linker, allocator, and boot invariants kept distinct.
- 10% reproducible artifact chain with deterministic diagnostics.

## Safety and limits

Use course-produced objects, disposable arenas, and the emulator. Do not execute linked learner bytes natively or use real unauthenticated network boot. Treat checksums as accidental-corruption detection only.

## Completion evidence

Submit objective score, annotated stage artifacts, link-map calculation, heap trace, minimal reproducer, patch, and regression output.

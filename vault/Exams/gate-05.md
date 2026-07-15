---
id: "gate-05"
title: "Operating System Gate"
section: "exams"
tags: ["exam", "mmu", "kernel", "filesystem"]
---

# Operating System Gate

## Purpose

This gate tests protection, process/resource ownership, block I/O, FAT integrity, and userland behavior as one layered system. The investigation rewards locating the earliest broken contract rather than patching filesystem bytes blindly.

## Objective knowledge

Run `python3 ftt exam gate-05`, answer from state and ownership invariants, then grade with the command shown. Explain every miss using a page-table, descriptor, or cluster-chain sketch.

## Practical investigation

After one child process writes a file and exits, another process faults while reading it; reboot then reveals a cyclic FAT chain. You receive a scheduler/syscall trace, process descriptor tables, page-table and TLB snapshots, block requests, and before/after disk-image sectors.

Predict the user-buffer translations, open-file references, sector writes, cluster-chain changes, and process states. Find the first contradiction in time. Determine whether the initiating defect is stale translation, unchecked copy range, shared-offset misuse, incomplete block write handling, or filesystem update ordering.

Repair one owning layer and add tests for page-crossing user buffers, forked descriptors, partial block write, FAT cycle, process exit during I/O, and reboot consistency. Demonstrate that resources return to baseline.

## Rubric

- 20% correct cross-layer state prediction.
- 30% earliest broken protection/ownership/storage contract localized.
- 25% transactional repair and adversarial regression tests.
- 15% resource and filesystem invariants after failure and reboot.
- 10% clear timeline correlating syscall, translation, block, and disk evidence.

## Safety and limits

Use the emulator and disposable disk-image copies only. Never mount or modify valuable media, expose kernel adapters beyond localhost, or suppress a fault to force progress.

## Completion evidence

Keep objective score, process/page/descriptor diagrams, sector diff, first-divergence timeline, repaired image check, and cleanup counts.

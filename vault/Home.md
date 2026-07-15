---
title: "From the Transistor to the Web Browser"
tags: ["course", "home"]
---

# From the Transistor to the Web Browser

Build one inspectable computer from bytes and gates to a small operating system and text web browser. The main path is software-first: every required checkpoint runs locally and deterministically without an FPGA, privileged networking, or Internet access.

## Start here

1. Read [[Learner Guide]].
2. Open [[Course Map]] and inspect the dependency spine.
3. Begin with [[00.01 Course Orientation]]. Do not skip the C runway because later failures often look like hardware or kernel bugs when they are pointer, signedness, or ABI bugs.
4. Use the active module's **Start here** source when its task needs another explanation; [[Reference Shelf]] collects every task-specific source in one place.
5. Keep [[Glossary]] open and add your own examples to a separate learning journal.

From the repository root, establish the baseline:

```sh
python3 ftt doctor
python3 ftt validate
python3 ftt list
python3 ftt next
```

`doctor` checks both course structure and local tools. `validate` checks authored data and links. A module's automated lab, when one exists, checks only that bounded implementation—not whether you can explain it.

## The evidence rule

A block is complete when you can provide all three:

- a working artifact or trace;
- a failing case you can explain and reproduce;
- a short explanation of the invariant that prevents that failure.

Passing tests without an explanation is incomplete. An explanation without executable evidence is also incomplete.

## Safety and scope

- Core work uses simulated RAM, packet fixtures, disk images, and local fixture servers.
- Never expose the course telnet service to a real network.
- Treat all binary, filesystem, packet, and image lengths as hostile input.
- The physical section is optional. Do not improvise mains-powered reflow, connect unknown voltage levels, or power an unreviewed custom board.
- Keep known-good checkpoints. Change one layer at a time and record the first divergent cycle, instruction, syscall, sector, or packet.

## Navigation

- [[Course Map]] — sections, adaptations, dependencies, and gates
- [[Notebook Guide]] — executable cross-level integration from bytes to physical bringup
- [[Challenge Atlas]] — 64 unusual hard problems with adversarial campaigns, boss handoffs, and replayable evidence
- [[Learner Guide]] — commands, study loop, evidence, and recovery
- [[Reference Shelf]] — English courses, manuals, specifications, and project references tied to concrete tasks
- [[Glossary]] — shared vocabulary from C through networking
- [[Capstone - Browser in a Box|Browser in a Box]] — final integration contract and fault campaign
- [[Workbook Entry]] and [[Lab Report]] — reusable Obsidian note templates
- [[Depth Audit and Geohot Alignment]] — honest baseline counts and the boundary between alignment and attribution
- [[Scope Decisions]], [[Original Syllabus]], and [[realhw Branch Study]] — what changed, the preserved outline, and a partial historical hardware trace reconstructed as tested contracts

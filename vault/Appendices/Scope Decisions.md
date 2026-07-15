---
id: "appendix-scope-decisions"
title: "Scope Decisions"
section: "appendices"
tags: ["appendix", "scope", "software-first", "safety"]
---

# Scope Decisions

The original outline has a compelling through-line: explain a modern software stack by constructing each layer below it. Its twelve-week estimate and several component choices do not fit a learner who is new to C or a course that must run from an ordinary checkout. This appendix makes the revised boundary explicit.

## Core promise

The required path is deterministic, inspectable, offline-capable, and runnable with Python, a C compiler, and repository fixtures. It teaches the same contracts as the proposed machine without requiring an FPGA, root access, raw networking, valuable removable media, custom electronics, or execution of unknown native input.

Every block follows one evidence loop:

1. predict state or bytes before execution;
2. run a bounded model or tool;
3. find the first divergence;
4. repair the owning layer;
5. add a regression and state the invariant;
6. preserve an artifact that a reviewer can inspect.

## Decisions by subsystem

| Area | Software-first core | Stretch or excluded production scope | Reason |
|---|---|---|---|
| C preparation | A dedicated C runway covers values, pointers, representation, ownership, ABI, diagnostics, and state machines. | None of the later systems blocks may be the learner's first substantial C program. | The original bootloader-first-C ordering hides too many simultaneous failure modes. |
| Instruction set | The FTT-16 teaching ISA, assembler, and traceable emulator define one compact, executable contract. | ARM reverse-engineering comparisons and established-ISA ports are optional. | The original moves from ARM7 to an “ARM9ish” MMU without one stable architecture contract. |
| RTL | Logic, UART, and CPU concepts have deterministic software models; synthesizable RTL can be compared at stable boundaries. | Pipelining, full compatibility, timing closure, and physical controllers are optional. | The core must remain runnable without HDL tools or hardware. |
| Compiler | A documented C0 subset and staged compiler are the required artifact. Python is the orchestration/reference language. | A Haskell implementation and broader ISO C are comparative extensions. | The learner's target is C and systems reasoning, not simultaneous mastery of Haskell and full C semantics. |
| Linker/runtime | A bounded object/ELF profile, static linking, freestanding libc subset, and invariant-checked allocator are core. | Complete ELF compatibility, all libc, and production allocator hardening are excluded. | Explicit narrow formats can be fully tested and explained. |
| Ethernet and boot | MMIO rings, frame fixtures, PCAP evidence, and a simulated bounded loader are core. | Real PHY timing and unauthenticated boot on a real network are stretch work. | Packet ownership and validation do not require electrical dependencies or network exposure. |
| MMU and OS | Reference translation, TLB behavior, a single-core deterministic kernel, scoped syscalls, and isolated processes are core. | SMP, signals, users, production security, and full POSIX are excluded. | A coherent small kernel teaches more than a broad but untestable syscall list. |
| Storage and FAT | A file-backed block device, fault injection, disposable images, and a fixed FAT profile are core. | Direct access to real disks and recovery of valuable media are forbidden. | Corruption tests must be repeatable and non-destructive. |
| TCP and services | Deterministic packet simulation and localhost fixture services are core. | Public bind shells, arbitrary Internet exposure, production TCP completeness, and TLS are excluded. | Loss/reordering logic can be tested without creating an insecure service. |
| Browser | Static-link-capable local HTTP, constrained HTML, text layout, safe terminal output, and link navigation are core. | CSS, JavaScript, images, cookies, authentication, and production Web compatibility are excluded. | The capstone must be bounded enough to investigate end to end. |
| Dynamic linking | One teaching shared-library profile is optional within the software course. | It cannot block the browser, which retains a static path. | Runtime relocation is valuable but not required to demonstrate the vertical slice. |
| Physical hardware | Simulated JTAG, declarative board review, and fault-injected bringup records are sufficient. A supported development board is the preferred real target. | Custom BGA PCB fabrication, reflow, USB firmware, real PHY/SD controllers, and unsupervised first power are optional separate EE work. | Procurement, electrical risk, and specialist review must not gate software learning. |

## Safety boundaries

- Course network services bind to loopback and use fixtures.
- Disk and filesystem work uses temporary copies, never host block devices.
- Downloaded or linked target bytes execute only in the course machine or an explicitly isolated oracle.
- Lab runners use argument arrays rather than a shell, but learner programs are not a hostile-code sandbox.
- Physical work requires voltage/ground verification, current limiting, stop conditions, and experienced review.
- A checksum detects accidental corruption; it is not authentication or secure boot.

## What “complete” means

Completion is not a line count and not a green happy-path demo. A block is complete when its learner can:

- predict a representative trace or byte layout;
- produce the declared artifact;
- pass normal, boundary, malformed-input, and fault-injection checks;
- diagnose one seeded failure from the first divergence;
- explain the key invariant and known limitations;
- show that the artifact composes with the next layer.

The optional physical track does not change core completion. The course's culminating evidence is a local text browser plus system traces connecting its request and rendered page back through the learner's runtime, kernel, storage/network models, toolchain, and machine abstractions.

## Relationship to the source

[[Original Syllabus]] remains the historical record. The numbered sections and source ideas are preserved, but the active [[Course Map]] is mastery-paced and software-first. Changes in implementation language, architecture, schedule, or hardware requirement are deliberate scope decisions, not silent omissions.

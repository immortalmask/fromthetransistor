---
title: "Hard Track 05 - Kernel and Storage Failure Laboratory"
tags: ["course", "challenge", "hard-track", "stage-05"]
---

# Hard Track 05: Kernel and Storage Failure Laboratory

Attack translation, privilege, traps, scheduling, partial I/O, persistence, and FAT until a multiprocess machine reboots explainably.

**Entry gate:** Complete modules 05.01 through 05.05, gate-05, and boot the H04 bundle.

**Stage handoff:** A syscall ABI, deterministic kernel trace, kernel ELF, disposable root image, and power-failure corpus.

Use `python3 ftt challenge start ID` to create an evidence workspace. The
checker replays positive and negative commands and verifies every claimed
artifact by hash; it cannot replace the engineering judgment in the rubric.

### Difficulty ladder

- `*` — focused: one main artifact and a narrow adversarial campaign.
- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.
- `***` — boss-scale: integrates the stage and produces the handoff consumed later.

## H05.01 · \* · Page-Walk Doppelganger

**Focused · Brutal · 34–51 hours · integration**

**Prerequisites:** 05.01, H03.03, H04.08

Compare a pure page walk with a bounded TLB over generated mappings, permissions, and malformed entries.

**Artifact:** reference walker, TLB path, table generator, and trace

### Deliverables

- A working reference walker, TLB path, table generator, and trace with reproducible instructions.
- An independent state or storage oracle plus seeded fault schedules.
- A replayable evidence packet with full event and durability traces.

### Constraints

- All execution and I/O are deterministic and explicitly bounded.
- Kernel boundaries validate user and disk bytes before mutation.
- Disk tests operate only on fresh disposable image copies.

### Adversarial campaign

- present page denying access
- malformed nonleaf
- offset-preservation edge

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic isolation and persistence checks.
- **A2:** Every adversarial schedule replays with precise state, fault, or durability evidence.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared kernel and root-image handoff directly.

**Handoff:** Translation and fault schemas become the kernel memory boundary.

**Safety:** Storage campaigns use disposable image copies only; never open host block devices.

## H05.02 · \* · Stale-Translation Escape

**Focused · Brutal · 30–45 hours · adversary**

**Prerequisites:** 05.01, H05.01

Attack stale TLB entries through remap, permission downgrade, ASID reuse, and invalidation schedules.

**Artifact:** invalidation model, attack scheduler, and minimized corpus

### Deliverables

- A working invalidation model, attack scheduler, and minimized corpus with reproducible instructions.
- An independent state or storage oracle plus seeded fault schedules.
- A replayable evidence packet with full event and durability traces.

### Constraints

- All execution and I/O are deterministic and explicitly bounded.
- Kernel boundaries validate user and disk bytes before mutation.
- Disk tests operate only on fresh disposable image copies.

### Adversarial campaign

- permission removed without flush
- ASID reused
- one page remapped while another stays hot

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic isolation and persistence checks.
- **A2:** Every adversarial schedule replays with precise state, fault, or durability evidence.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared kernel and root-image handoff directly.

**Handoff:** The invalidation protocol becomes a context-switch assertion.

**Safety:** Storage campaigns use disposable image copies only; never open host block devices.

## H05.03 · \*\* · Hostile Exec and Syscall Boundary

**Cumulative · Brutal · 38–57 hours · adversary**

**Prerequisites:** 05.02, H04.05, H05.01

Load hostile ELF and validate user buffers spanning pages with precise fault atomicity.

**Artifact:** ELF loader, user-copy layer, malformed corpus, and fault ledger

### Deliverables

- A working ELF loader, user-copy layer, malformed corpus, and fault ledger with reproducible instructions.
- An independent state or storage oracle plus seeded fault schedules.
- A replayable evidence packet with full event and durability traces.

### Constraints

- All execution and I/O are deterministic and explicitly bounded.
- Kernel boundaries validate user and disk bytes before mutation.
- Disk tests operate only on fresh disposable image copies.

### Adversarial campaign

- segment range wrap
- buffer ending on absent page
- overlapping incompatible segments

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic isolation and persistence checks.
- **A2:** Every adversarial schedule replays with precise state, fault, or durability evidence.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared kernel and root-image handoff directly.

**Handoff:** Loader and user-copy rules become the syscall boundary.

**Safety:** Storage campaigns use disposable image copies only; never open host block devices.

## H05.04 · \*\* · Trap and Scheduler Replay

**Cumulative · Brutal · 42–63 hours · integration**

**Prerequisites:** 05.02, H03.05, H05.02, H05.03

Record traps, switches, address spaces, and wakeups so seeded preemption replays identically.

**Artifact:** scheduler, event log, replay engine, and lost-wakeup mutant

### Deliverables

- A working scheduler, event log, replay engine, and lost-wakeup mutant with reproducible instructions.
- An independent state or storage oracle plus seeded fault schedules.
- A replayable evidence packet with full event and durability traces.

### Constraints

- All execution and I/O are deterministic and explicitly bounded.
- Kernel boundaries validate user and disk bytes before mutation.
- Disk tests operate only on fresh disposable image copies.

### Adversarial campaign

- preemption during copy
- child exit beside wait
- switch with hot TLB

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic isolation and persistence checks.
- **A2:** Every adversarial schedule replays with precise state, fault, or durability evidence.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared kernel and root-image handoff directly.

**Handoff:** The event schema becomes the process investigation trace.

**Safety:** Storage campaigns use disposable image copies only; never open host block devices.

## H05.05 · \*\* · Partial-I-O State Machine

**Cumulative · Very Hard · 30–45 hours · adversary**

**Prerequisites:** 05.02, H05.03, H05.04

Implement read, write, pipe, wait, and close under short progress, interruption, exit, and descriptor reuse.

**Artifact:** syscall state machines, process scripts, and leak report

### Deliverables

- A working syscall state machines, process scripts, and leak report with reproducible instructions.
- An independent state or storage oracle plus seeded fault schedules.
- A replayable evidence packet with full event and durability traces.

### Constraints

- All execution and I/O are deterministic and explicitly bounded.
- Kernel boundaries validate user and disk bytes before mutation.
- Disk tests operate only on fresh disposable image copies.

### Adversarial campaign

- short write then exit
- reader with final writer gone
- descriptor reused after interruption

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic isolation and persistence checks.
- **A2:** Every adversarial schedule replays with precise state, fault, or durability evidence.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared kernel and root-image handoff directly.

**Handoff:** The syscall ABI feeds shell, Telnet, and browser processes.

**Safety:** Storage campaigns use disposable image copies only; never open host block devices.

## H05.06 · \*\* · Power-Cut Block Device

**Cumulative · Brutal · 36–54 hours · adversary**

**Prerequisites:** 05.03, H04.07

Inject timeout, torn write, reorder, short completion, and crash at every sector operation.

**Artifact:** file-backed device, fault scheduler, replay log, and durability model

### Deliverables

- A working file-backed device, fault scheduler, replay log, and durability model with reproducible instructions.
- An independent state or storage oracle plus seeded fault schedules.
- A replayable evidence packet with full event and durability traces.

### Constraints

- All execution and I/O are deterministic and explicitly bounded.
- Kernel boundaries validate user and disk bytes before mutation.
- Disk tests operate only on fresh disposable image copies.

### Adversarial campaign

- half-sector persists
- writes reach media reversed
- crash between metadata and data

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic isolation and persistence checks.
- **A2:** Every adversarial schedule replays with precise state, fault, or durability evidence.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared kernel and root-image handoff directly.

**Handoff:** The block API and crash corpus become the FAT storage contract.

**Safety:** Storage campaigns use disposable image copies only; never open host block devices.

## H05.07 · \*\* · FAT Forensic Recovery

**Cumulative · Brutal · 36–54 hours · archaeology**

**Prerequisites:** 05.04, H00.01, H05.06

Diagnose loops, cross-links, lost clusters, and torn directories, recovering files only to a new image.

**Artifact:** FAT checker, forensic report, recovered image, and host transcript

### Deliverables

- A working FAT checker, forensic report, recovered image, and host transcript with reproducible instructions.
- An independent state or storage oracle plus seeded fault schedules.
- A replayable evidence packet with full event and durability traces.

### Constraints

- All execution and I/O are deterministic and explicitly bounded.
- Kernel boundaries validate user and disk bytes before mutation.
- Disk tests operate only on fresh disposable image copies.

### Adversarial campaign

- cyclic cluster chain
- two files share cluster
- inconsistent LFN sequence

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic isolation and persistence checks.
- **A2:** Every adversarial schedule replays with precise state, fault, or durability evidence.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared kernel and root-image handoff directly.

**Handoff:** The verified root image becomes persistent user-space input.

**Safety:** Storage campaigns use disposable image copies only; never open host block devices.

## H05.08 · \*\*\* · Boss: Persistent Multiprocess Machine

**Boss-Scale · Brutal · 56–84 hours · boss**

**Prerequisites:** H05.02, H05.03, H05.04, H05.05, H05.06, H05.07

Boot, run a fork-exec pipeline, persist a file, inject a block fault, reboot, and explain surviving state.

**Artifact:** kernel ELF, root image, session, reboot trace, and ledger

### Deliverables

- A working kernel ELF, root image, session, reboot trace, and ledger with reproducible instructions.
- An independent state or storage oracle plus seeded fault schedules.
- A replayable evidence packet with full event and durability traces.

### Constraints

- All execution and I/O are deterministic and explicitly bounded.
- Kernel boundaries validate user and disk bytes before mutation.
- Disk tests operate only on fresh disposable image copies.

### Adversarial campaign

- process fault during write
- metadata block timeout
- stale-TLB mutant on reboot

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic isolation and persistence checks.
- **A2:** Every adversarial schedule replays with precise state, fault, or durability evidence.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the declared kernel and root-image handoff directly.

**Handoff:** Kernel, syscall ABI, trace, and root image pass to networking.

**Safety:** Storage campaigns use disposable image copies only; never open host block devices.

## Primary references

- [RISC-V supervisor ISA](https://docs.riscv.org/reference/isa/priv/supervisor.html) — Ground translation, privilege, traps, faults, and invalidation in a precise contract.
- [Virtio 1.3 block specification](https://docs.oasis-open.org/virtio/virtio/v1.3/virtio-v1.3.html) — Define bounded request, completion, status, and ownership behavior.
- [POSIX exec specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html) — Scope process replacement, descriptors, arguments, and failure behavior.
- [ECMA-107 filesystem standard](https://ecma-international.org/publications-and-standards/standards/ecma-107/) — Compare official disk structures with the bounded FAT reasoning.

Return to [[Challenge Atlas]].

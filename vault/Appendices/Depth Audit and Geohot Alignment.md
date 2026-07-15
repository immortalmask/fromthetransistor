---
title: "Depth Audit and Geohot Alignment"
tags: ["course", "audit", "geohot", "practice", "hard-track"]
---

# Depth Audit and Geohot Alignment

## Short verdict

The software-first core is a strong C-beginner runway and a broad map of the
computer stack. Before the hard track was added, it was **not** equivalent in
construction depth to the historical project outline and it did not yet supply
a large reverse-engineering corpus. The honest description is:

- **conceptually aligned:** every layer feeds the next, from logic to browser;
- **deliberately narrowed:** small deterministic host-side models replace most
  whole subsystems and physical work;
- **not attributable pedagogy:** the repository shows Geohot's outline and an
  incomplete experiment, not a delivered course whose exact teaching method can
  be reconstructed.

The new [[Challenge Atlas]] addresses the problem-count and evidence gap with 64
hard problems. It does not magically turn every brief into a supplied reference
implementation; the status boundary is recorded below.

## What the primary artifacts actually establish

[The pinned software-first README](https://github.com/geohot/fromthetransistor/blob/905e22db2f91df6b968de10c24eb339b8ea1fca3/README.md) says that
the projects should build on one another and sketches an ARM7 CPU, C compiler,
linker, libc/allocator, Ethernet controller, bootloader, MMU, Unix-like OS,
storage, FAT, TCP, dynamic linking, browser, JTAG, board design, and bringup. Its
rough line estimates total about 11,200 across Verilog, Python, Haskell,
assembly, and C. Line counts are not a quality measure; here they reveal the
order-of-magnitude difference between a component exercise and the proposed
whole component.

[The `realhw` branch](https://github.com/geohot/fromthetransistor/tree/realhw)
shows an exploratory restart around a Spartan-6 board: vendor documentation,
an LED synthesis experiment, and early USB/SPI-flash probing. It also records
design questions about language choice, FPGA/toolchain choice, processor scope,
and C semantics. It does **not** contain later CPU, compiler, OS, TCP, or browser
implementations. Therefore “historically aligned” is supportable; “the complete
course Geohot intended” is not.

That boundary is reinforced by Geohot's own repository comments: he described
the goal as understanding the whole stack rather than training one narrow
abstraction, but also said that material still needed to be found and written
while staying only about a week ahead. See
[issue 2](https://github.com/geohot/fromthetransistor/issues/2#issuecomment-239855492)
and [issue 1](https://github.com/geohot/fromthetransistor/issues/1#issuecomment-239702570).
The later note about a possible livestream is likewise a proposal, not evidence
that a complete course was delivered.

See [[Original Syllabus]], [[realhw Branch Study]], and [[Scope Decisions]] for
the preserved outline and adaptation details.

## Baseline practice inventory

This snapshot was measured before the 64-problem hard track was added.

| Stage | Modules | Problem-set prompts | Homework steps | Executable labs | Modules without a lab |
|---|---:|---:|---:|---:|---:|
| 00 C Runway | 8 | 40 | 40 | 1 | 7 |
| 01 Intro | 2 | 10 | 10 | 1 | 1 |
| 02 Bringup | 2 | 10 | 11 | 1 | 1 |
| 03 Processor | 3 | 18 | 19 | 2 | 1 |
| 04 Toolchain | 5 | 30 | 31 | 3 | 2 |
| 05 OS | 5 | 30 | 32 | 2 | 3 |
| 06 Browser | 4 | 24 | 29 | 1 | 3 |
| 07 Physical | 3 | 18 | 19 | 1 | 2 |
| **Total** | **32** | **180** | **about 191** | **12** | **20** |

The 12 labs have 119 deterministic black-box cases, native C suites, strict C17
warnings, intentionally failing starters, and an undefined-behavior sanitizer
pass. Those are real strengths. Their 12 reference implementations total about
1,953 C lines; eleven are 59–236 lines and the browser lab is 523 lines.

## Where the baseline became shallow

The written homework often names a substantial subsystem, but the checked lab
tests one boundary-sized slice:

| Module ambition | Checked lab slice |
|---|---|
| Compiler with tokens, AST, types, statements, control flow, and target code | One arithmetic-expression parser and stack-code emitter |
| ELF linker with sections, symbols, layout, and relocations | One `abs32` or `rel32` calculation |
| libc plus free-list allocator, split/coalesce, and allocation-failure tests | A 64-byte bump arena without `free` |
| FAT allocation, chains, files, deletion, and consistency checks | Decode one 32-byte directory entry |
| Incremental HTTP, HTML tree/layout, links, redirects, and fragmentation | Render one complete response in a small HTML subset |
| JTAG instructions, shifting, replay, and transport faults | Compute TAP transitions from a TMS bit string |

This makes the labs useful prerequisites, not proof that the large homework was
built. Before the hard track, reverse-engineering had the same problem: every
module offered a good investigation prompt, but the repository did not bundle
the promised unknown binaries, objects, waveforms, packet captures, disk images,
or board manifests.

## What the hard track changes

[[Challenge Atlas]] adds eight problems at every stage, with archaeology,
construction, adversarial, integration, and boss lanes. Each problem specifies:

- an artifact that becomes input to later stages;
- at least three adversarial cases and four acceptance criteria;
- a positive and negative replay requirement;
- hashed evidence, first-divergence analysis, an invariant, and limitations;
- a simulation/offline lane whenever hardware or networking is involved.

The `ftt challenge` runner creates a workspace and rejects incomplete evidence.
It confines paths, verifies SHA-256 hashes, and executes declared argument arrays
without a shell under short timeouts. This closes the old “any nonempty manual
claim counts as completion” weakness for the hard track.

## Remaining boundary

The hard track is now a large, specific, testable problem curriculum and its
evidence protocol is executable. Most of its 64 subsystem implementations,
mutation farms, and forensic fixture corpora are intentionally learner work;
they are not 64 pre-solved labs. A future fixture expansion should begin with
H00, H01, and H03, then make every stage boss import the learner artifacts from
the previous boss. Until that exists, describe the repository as:

> a verified beginner core plus a rigorous advanced challenge specification and
> replayable self-validation system—not a finished clone of an undocumented
> Geohot course.

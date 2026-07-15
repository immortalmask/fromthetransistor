---
id: "04"
title: "Section 04: Compiler and Runtime"
section: "04"
tags: ["moc", "compiler", "toolchain"]
---

# Section 04: Compiler and Runtime

This section turns source text into a checked boot image. Each block preserves an inspectable intermediate artifact so a failure can be localized instead of blamed on “the compiler.”

1. [[04.01 C Compiler]] — define and implement a small, explicit C subset.
2. [[04.02 ELF Linker]] — lay out sections, resolve symbols, and apply relocations.
3. [[04.03 Freestanding libc and Allocator]] — supply the runtime that hosted C normally hides.
4. [[04.04 Ethernet Controller]] — model frames, descriptor ownership, and MMIO queues.
5. [[04.05 Network Bootloader]] — validate, place, and transfer control to an image.

The dependency chain is deliberate: compiler output feeds the linker; linked programs depend on the runtime; the controller transports bytes; the bootloader decides whether those bytes may execute.

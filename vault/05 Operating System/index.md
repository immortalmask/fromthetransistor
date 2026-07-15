---
id: "05"
title: "Section 05: Operating System"
section: "05"
tags: ["moc", "operating-system", "storage"]
---

# Section 05: Operating System

This section builds protection and persistent process state from explicit mechanisms. Each module exposes a traceable contract rather than hiding behavior behind a host operating system.

1. [[05.01 MMU and Page Tables]] — translate, protect, fault, and invalidate.
2. [[05.02 Unix-like Operating System]] — traps, processes, file descriptors, scheduling, and virtual memory.
3. [[05.03 SD Card and Block Device]] — a faultable fixed-size storage interface.
4. [[05.04 FAT Filesystem]] — interpret and safely update an interoperable disk image.
5. [[05.05 Init Shell and Utilities]] — exercise the system through ordinary user programs.

The section is complete when two isolated programs can manipulate persistent files through system calls and failures remain attributable to one layer.

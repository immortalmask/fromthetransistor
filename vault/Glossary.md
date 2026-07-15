---
title: "Glossary"
tags: ["course", "reference"]
---

# Glossary

Terms are defined in the narrow sense used by this course.

## C and representation

**ABI (application binary interface)** — The machine-level contract for calls, registers, stack alignment, object layout, and executable conventions.

**Alignment** — A requirement or preference that an object address be a multiple of some power of two. Alignment is distinct from size.

**Byte order / endianness** — The order in which a multi-byte integer's bytes appear at increasing addresses. It does not reverse bits inside a byte.

**Defined behavior** — Behavior for which the C implementation provides a specified meaning. Contrast with implementation-defined, unspecified, and undefined behavior.

**Lifetime** — The interval during which an object exists and may legally be accessed. A numerically unchanged address does not extend lifetime.

**Object file** — Compiler/assembler output containing sections, symbols, and relocation requests, not yet a complete process image.

**Ownership** — A course convention naming the component responsible for eventually releasing or transferring a resource. C does not enforce it.

**Pointer provenance** — The association between a pointer and the storage/object from which it was derived; an integer-looking address alone is not a universal access permit.

**Relocation** — A request to patch encoded data or an instruction once final symbol addresses are known.

**Section / segment** — A section organizes link-time content; a segment describes how ranges are loaded into memory at runtime.

**Sign extension** — Replicating a signed value's top bit when widening it. Zero extension fills the new upper bits with zero.

**Undefined behavior** — A C operation for which the language imposes no requirements, such as many out-of-bounds accesses or invalid shifts.

## Digital logic and processor

**Architectural state** — State visible in the ISA contract: program counter, registers, memory effects, privilege state, and defined control registers.

**Combinational logic** — Output determined by current input without clocked storage in the abstract model.

**Cycle** — One clock period. A simulator may execute many internal events during a cycle.

**Flip-flop / register** — Clocked storage that captures a value at a defined edge.

**FSM (finite-state machine)** — A finite set of states plus transition and output rules.

**ISA (instruction set architecture)** — The software-visible instruction encodings and effects. It is not the same thing as a particular processor implementation.

**LUT (lookup table)** — FPGA resource implementing a small Boolean function by indexing stored truth-table bits.

**MMIO (memory-mapped I/O)** — Device registers selected through address-space loads and stores. Reads and writes may have side effects unlike RAM.

**RTL (register-transfer level)** — A hardware model organized around registers, combinational transformations, and clocked transfers.

**Semihosting** — A simulator or debugger intercepts a target operation and performs a host service. Useful for tests, but not a real target device path.

**Trap** — A controlled transfer to privileged software caused by an exception, interrupt, fault, or system-call instruction.

**UART** — An asynchronous byte-oriented serial interface that frames data with start, data, optional parity, and stop bits.

**VCD / waveform** — A timestamped signal trace used to inspect hardware simulation behavior.

## Toolchain and runtime

**AST (abstract syntax tree)** — A tree representing parsed language structure after punctuation not needed by later phases is removed.

**Code generation** — Translation from a typed or lowered representation into target instructions or assembly.

**ELF** — A family of object and executable formats describing headers, sections, segments, symbols, and relocations.

**Freestanding C** — C execution without assuming a host operating system or complete standard library.

**GOT / PLT** — Tables and stubs commonly used to address dynamically resolved data and functions in position-independent code.

**Linker** — Tool that combines object files, resolves symbols, lays out addresses, applies relocations, and emits an image.

**Loader** — Code that maps an executable or shared object into memory and establishes its initial runtime state.

## Operating system and storage

**Address space** — The virtual addresses and mappings visible to a process or privilege context.

**Context switch** — Saving one execution context and restoring another according to a defined register/state contract.

**FAT** — A filesystem family using allocation tables to chain clusters. This course targets a bounded FAT16 profile.

**Page fault** — A trap raised when translation is absent, malformed, or violates access permissions.

**Process** — An execution context with resources and an address-space identity. It is more than a stack or user-level thread.

**Sector** — The fixed-size transfer unit exposed by the course block device.

**Syscall** — A checked transition from user code into a kernel service.

**TLB (translation lookaside buffer)** — A cache of recent virtual-to-physical translations and permissions.

**VFS (virtual filesystem)** — Kernel interface that presents common file operations while delegating storage-specific behavior.

## Networking and physical systems

**ARP** — IPv4 local-network protocol mapping an IP address to an Ethernet MAC address.

**Checksum** — Redundant value used to detect accidental corruption. It is not authentication.

**Ethernet frame** — Link-layer destination/source addresses, type/length, payload, and link integrity data.

**HTTP** — Application protocol carrying requests and responses. The core browser uses a deliberately limited, non-TLS profile.

**JTAG / TAP** — A serial test/access protocol and its standardized state machine, often used to configure or debug devices.

**PCAP** — Packet capture representation used here as replayable network evidence.

**TCP** — Ordered byte-stream transport built from sequence numbers, acknowledgements, retransmission, flow control, and connection state.

**TLS** — Cryptographic transport security. It is explicitly outside the core browser scope.

**TOCTOU** — Time-of-check-to-time-of-use error in which validated state changes before use; relevant across devices, interrupts, and shared resources.

---
title: "Reference Shelf"
tags: ["ftt", "references", "sources"]
---

# Reference Shelf

Links last verified: 2026-07-15.

This shelf mirrors each module's short source list. **Start here** items are
the approachable entry point; **Reference** items answer exact contract questions;
**Go deeper** items are for comparison or extension. Read only the portion named
by the task. A specification is rarely the best first explanation.

See [[Scope Decisions]] for the boundary between the software core and optional
hardware work.

## 00 — C Runway

### [[00.01 Course Orientation]]

- **Start here · Course:** [From Nand to Tetris: Course Projects](https://www.nand2tetris.org/course) — Use the twelve-project dependency chain to refine the workbook sketch from terminal output down through software, ISA, memory, and logic boundaries.
- **Go deeper · Course:** [MIT 6.004 Computation Structures](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) — Use the course sequence to populate the trace-vocabulary table with concrete units of progress from gates through processors, devices, and systems.
- **Reference · Manual:** [Pro Git: About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control) — Use this when defining clean baselines and reversible checkpoints for the homework's deliberate validation failure and restoration.

### [[00.02 Shell Build and Debug Loop]]

- **Start here · Course:** [MIT Missing Semester: Course Overview and the Shell](https://missing.csail.mit.edu/2020/course-shell/) — Use the shell, quoting, redirection, and process examples while predicting commands and separating output, diagnostics, and exit status.
- **Go deeper · Course:** [MIT Missing Semester: Debugging and Profiling](https://missing.csail.mit.edu/2020/debugging-profiling/) — Use its debugger workflow to turn the deliberately broken homework program into a reproducible causal trace rather than a symptom report.
- **Reference · Manual:** [GCC Warning Options](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html) — Look up every strict-build warning before changing code, especially conversion, signedness, return-type, and unused-value diagnostics.
- **Reference · Manual:** [GCC Instrumentation Options](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html) — Use the AddressSanitizer and UndefinedBehaviorSanitizer sections to build and interpret the required out-of-bounds failure trace.

### [[00.03 C Values and Control Flow]]

- **Start here · Course:** [Beej's Guide to C Programming: Types III — Conversions](https://beej.us/guide/bgc/html/split/types-iii-conversions.html) — Use the integer-promotion, signed/unsigned-conversion, and strtol sections to trace the workbook expressions and reject trailing input.
- **Start here · Course:** [Beej's Guide to C Programming: Fixed-Width Integer Types](https://beej.us/guide/bgc/html/split/fixed-width-integer-types.html) — Use this to complete the host range table and distinguish exact-width types from least-width, fast, and ordinary integer types.
- **Reference · Specification:** [SEI CERT C INT30-C: Ensure Unsigned Integer Operations Do Not Wrap](https://wiki.sei.cmu.edu/confluence/spaces/c/pages/87152236/INT30-C.%2BEnsure%2Bthat%2Bunsigned%2Binteger%2Boperations%2Bdo%2Bnot%2Bwrap) — Apply its precondition patterns to offset-plus-count validation and every size calculation in the field decoder.
- **Reference · Specification:** [SEI CERT C INT34-C: Validate Shift Counts](https://wiki.sei.cmu.edu/confluence/spaces/c/pages/87152418/INT34-C.%2BDo%2Bnot%2Bshift%2Ban%2Bexpression%2Bby%2Ba%2Bnegative%2Bnumber%2Bof%2Bbits%2Bor%2Bby%2Bgreater%2Bthan%2Bor%2Bequal%2Bto%2Bthe%2Bnumber%2Bof%2Bbits%2Bthat%2Bexist%2Bin%2Bthe%2Boperand) — Use its operand-width rules to justify the decoder's width-32 special case and every rejected shift boundary.

### [[00.04 Bytes Bits and Representation]]

- **Start here · Course:** [Beej's Guide to C Programming: Bitwise Operations](https://beej.us/guide/bgc/html/split/bitwise-operations.html) — Use the AND, OR, XOR, and shift examples before deriving masks and byte contributions in the workbook.
- **Reference · Specification:** [WG14 N1570 C Committee Draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) — Consult sections 6.2.6.1, 6.5.7, and 7.20.1.1 for object representation, shift semantics, and exact-width integer guarantees.
- **Reference · Manual:** [Linux Kernel Documentation: Unaligned Memory Accesses](https://docs.kernel.org/core-api/unaligned-memory-access.html) — Use the architecture examples to explain precisely why casting an arbitrary byte pointer to uint32_t pointer is not a portable decoder.
- **Go deeper · Manual:** [GNU Coreutils: od Invocation](https://www.gnu.org/software/coreutils/manual/html_node/od-invocation.html) — Use od as an independent byte-level oracle for the homework utility's offsets, hexadecimal bytes, character view, and endianness tests.

### [[00.05 Pointers Arrays and Strings]]

- **Start here · Course:** [Beej's Guide to C Programming: Pointers](https://beej.us/guide/bgc/html/split/pointers.html) — Use its address, dereference, and const examples to draw the workbook object diagrams before implementing the bounded buffer.
- **Start here · Course:** [Beej's Guide to C Programming: Arrays](https://beej.us/guide/bgc/html/split/arrays.html) — Use the array-to-pointer and function-parameter sections to explain the differing sizeof results and why a parameter cannot prove the supplied bound.
- **Start here · Course:** [Beej's Guide to C Programming: Strings](https://beej.us/guide/bgc/html/split/strings.html) — Use its terminator and storage examples when implementing exact-fit text copies, embedded-zero tests, and missing-terminator failures.
- **Reference · Specification:** [SEI CERT C ARR30-C: Do Not Form or Use Out-of-Bounds Pointers](https://wiki.sei.cmu.edu/confluence/display/c/ARR30-C.%2BDo%2Bnot%2Bform%2Bor%2Buse%2Bout-of-bounds%2Bpointers%2Bor%2Barray%2Bsubscripts) — Apply its pointer-validity cases to the cursor invariant, one-past pointer discussion, and attempted read-past-end tests.

### [[00.06 Structs Memory and Ownership]]

- **Start here · Course:** [Beej's Guide to C Programming: Structs](https://beej.us/guide/bgc/html/split/structs.html) — Use the struct, copying, comparison, and padding discussion before measuring offsets and writing the collection invariant.
- **Start here · Course:** [Beej's Guide to C Programming: Manual Memory Allocation](https://beej.us/guide/bgc/html/split/manual-memory-allocation.html) — Use its malloc, realloc, failure-checking, and free examples to stage the owned collection implementation.
- **Reference · Specification:** [SEI CERT C MEM35-C: Allocate Sufficient Memory for an Object](https://wiki.sei.cmu.edu/confluence/spaces/c/pages/87152128/MEM35-C.%2BAllocate%2Bsufficient%2Bmemory%2Bfor%2Ban%2Bobject) — Apply its sizeof and multiplication guards to every append allocation and forced-allocation-failure case.
- **Reference · Specification:** [SEI CERT C MEM31-C: Free Dynamically Allocated Memory When No Longer Needed](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/memory-management-mem/mem31-c/) — Use it to audit the constructor failure matrix and prove that destroy releases every owned allocation exactly once.

### [[00.07 Functions ABI and Object Files]]

- **Start here · Course:** [MIT 6.004: Procedures and Stacks](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c12/c12s1/) — Use the calling-convention and activation-record material to annotate arguments, saved state, return values, and stack movement in the workbook call trace.
- **Reference · Specification:** [ELF Object File Format](https://gabi.xinuos.com/) — Consult chapters 3, 5, 6, and 7 when classifying sections, symbols, relocations, and loadable segments in the object-file report.
- **Reference · Manual:** [GNU Binary Utilities: readelf](https://sourceware.org/binutils/docs/binutils/readelf.html) — Use readelf to capture section headers, symbol tables, and relocations before and after the final link.
- **Reference · Manual:** [GNU Binary Utilities: objdump](https://sourceware.org/binutils/docs/binutils/objdump.html) — Use objdump to follow one call through argument setup and return, then compare debug and optimized disassembly.

### [[00.08 Digital Logic and State Machines]]

- **Start here · Course:** [MIT 6.004: Combinational Logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c4/c4s1/) — Use the Boolean, mux, and combinational-circuit material to derive the workbook truth tables and LUT masks.
- **Start here · Course:** [MIT 6.004: Sequential Logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c5/c5s1/) — Use its clocked-state model to keep current value, computed next value, edge, and observed value separate in counter traces.
- **Start here · Course:** [MIT 6.004: Finite State Machines](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c6/c6s1/) — Use the FSM construction method for the IDLE-DATA-DONE workbook table and the two-edge request-controller homework.

## 01 — Intro

### [[01.01 Transistors Gates and LUTs]]

- **Start here · Course:** [MIT 6.004: The Digital Abstraction](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c2/c2s1/) — Use this to state what logic levels preserve and what analog voltage, timing, noise, and manufacturing details the lab deliberately hides.
- **Go deeper · Course:** [MIT 6.004: CMOS](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c3/c3s1/) — Use the MOS switch networks to justify the abstraction-map steps from controlled switch through inverter and logic gates.
- **Start here · Project:** [Nand2Tetris Project 1: Boolean Logic](https://www.nand2tetris.org/project01) — Use its staged gate and multiplexer construction as extra practical work after completing the exhaustive C LUT properties.
- **Reference · Manual:** [AMD UltraScale Architecture Configurable Logic Block User Guide UG574](https://docs.amd.com/r/en-US/ug574-ultrascale-clb) — Read the Look-Up Table and Storage Elements sections to connect the lab's abstract mask and counter to real FPGA LUT and register resources.

### [[01.02 Simulation and Waveforms]]

- **Start here · Manual:** [cocotb Documentation: The Timing Model](https://docs.cocotb.org/en/stable/timing_model.html) — Use simulator phases and triggers to repair the workbook test that changes an input at the same timestamp as the rising edge.
- **Reference · Manual:** [Verilator Guide: Trace Options](https://verilator.org/guide/latest/exe_verilator.html#cmdoption-trace) — Use the VCD or FST trace options when implementing the optional bounded harness and capturing the first divergent cycle.
- **Go deeper · Manual:** [GTKWave Documentation](https://gtkwave.github.io/gtkwave/) — Use it to load the generated trace, select only the clock-reset-state-output cone, and annotate the deliberate defect.

## 02 — Bringup

### [[02.01 Blinking an LED]]

- **Start here · Project:** [Nand2Tetris Project 3: Memory](https://www.nand2tetris.org/project03) — Use its register and counter exercises to reinforce edge-triggered state before writing the configurable LED-divider step model.
- **Reference · Manual:** [Intel Quartus Prime: Counter HDL Guidelines](https://www.intel.com/content/www/us/en/docs/programmable/683082/24-3/counter-hdl-guidelines.html) — Use the counter coding patterns to review the optional RTL implementation after the portable reference model passes.
- **Reference · Manual:** [Intel Quartus Prime: Use Synchronous Resets](https://www.intel.com/content/www/us/en/docs/programmable/683082/25-1/use-synchronous-resets.html) — Use its reset timing discussion to specify exactly what repeated assertion and between-edge deassertion mean in the homework trace.
- **Go deeper · Project:** [geohot/fromthetransistor realhw branch snapshot](https://github.com/geohot/fromthetransistor/tree/9ef169c4828d432db099cea5a76c24a4af4f526c) — Treat the partial Spartan-6 LED synthesis and SPI-flash exploration as a historical bring-up trace: identify unstated board, tool, reset, protocol, and validation assumptions, then replace them with the course's portable model, exact-cycle tests, and evidence manifest.

### [[02.02 UART and MMIO]]

- **Start here · Project:** [OpenTitan UART: Theory of Operation](https://opentitan.org/book/hw/ip/uart/doc/theory_of_operation.html) — Use its frame diagram and 16x receive sampling sequence to check the 8N1 encodings, sample edges, framing errors, and overrun model.
- **Reference · Project:** [OpenTitan UART: Register Reference](https://opentitan.org/book/hw/ip/uart/doc/registers.html) — Use the documented reset values and register side effects as a model for the homework's DATA and STATUS MMIO table.
- **Reference · Specification:** [WG14 N1570 C Committee Draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) — Read section 6.7.3 on volatile-qualified objects before explaining what volatile MMIO accesses guarantee and what ordering or atomicity they do not.

## 03 — Processor

### [[03.01 Assembler and ISA]]

- **Start here · Project:** [Nand2Tetris Project 6: The Assembler](https://www.nand2tetris.org/project06) — Use its staged symbol-free then symbolic implementation and independent comparison tool as the model for the FTT-16 two-pass assembler.
- **Reference · Specification:** [RISC-V RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html) — Study sections 2.1.2 and 2.1.3 to compare fixed fields, immediate reconstruction, reserved encodings, and signed control-flow offsets with FTT-16.
- **Go deeper · Manual:** [GNU Binutils: Using as](https://sourceware.org/binutils/docs/as/) — Use the Syntax, Symbols, Labels, and Expressions chapters when adding comments and labels without weakening operand validation.

### [[03.02 CPU Emulator]]

- **Start here · Project:** [Nand2Tetris Project 5: Computer Architecture](https://www.nand2tetris.org/project05) — Use its CPU-memory-program tests to plan incremental FTT-16 emulator tests before combining all instruction families.
- **Reference · Specification:** [RISC-V RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html) — Use the programmer's model and arithmetic, control-transfer, load, and store semantics as an example of separating architectural state from instruction encoding.
- **Go deeper · Project:** [Sail RISC-V Formal ISA Model](https://github.com/riscv/sail-riscv) — Study how encoders, decoders, instruction semantics, and an executable emulator derive from one precise model when designing an independent FTT-16 oracle.

### [[03.03 Boot ROM Monitor]]

- **Start here · Project:** [MCUboot Serial Recovery](https://docs.mcuboot.com/serial_recovery.html) — Use its length, framing, integrity, buffer, and timeout tradeoffs to design truncation recovery and resynchronization tests for the boot protocol.
- **Go deeper · Manual:** [U-Boot loadb Command](https://docs.u-boot.org/en/latest/usage/cmd/loadb.html) — Use this real monitor command as a comparison point for serial image reception, destination bounds, transfer results, and later execution.
- **Reference · Project:** [MCUboot Bootloader Design](https://docs.mcuboot.com/design.html) — Use its magic, little-endian headers, image slots, validation, RAM loading, and chain-loading flow to review the monitor's validate-then-commit invariant.

## 04 — Compiler

### [[04.01 C Compiler]]

- **Start here · Course:** [My First Language Frontend with LLVM Tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/) — Use chapters 1-3 and 5 to structure the lexer, recursive-descent parser, AST, code generation, and control-flow milestones; adapt the architecture to C0 and direct assembly output.
- **Reference · Manual:** [Clang CFE Internals Manual](https://clang.llvm.org/docs/InternalsManual.html) — Use its source-location, token, parser, AST, and diagnostic-testing sections to implement precise spans, deterministic errors, and malformed-input fixtures.
- **Reference · Specification:** [WG14 N2176: C17 Draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2176.pdf) — Use clauses 6.4, 6.5, and 6.8 to freeze lexical rules, precedence, short-circuit behavior, and statements for the supported C0 subset.
- **Go deeper · Project:** [chibicc](https://github.com/rui314/chibicc) — After completing each stage independently, compare its incremental tokenizer, parser, type checker, and code-generator boundaries and test organization.

### [[04.02 ELF Linker]]

- **Start here · Manual:** [GNU ld Manual](https://sourceware.org/binutils/docs/ld/) — Use the linker-script, SECTIONS, alignment, symbol, and map-file chapters as a concrete model for section merging, address assignment, and deterministic map output.
- **Reference · Specification:** [System V ABI: ELF Object File Format](https://gabi.xinuos.com/elf.pdf) — Use the ELF header, section table, string table, symbol table, relocation, and program-header definitions to derive bounded parsing and relocation formulas.
- **Reference · Manual:** [GNU readelf Manual](https://sourceware.org/binutils/docs/binutils/readelf.html) — Use readelf header, section, symbol, relocation, and segment views as an external oracle for linker acceptance tests.

### [[04.03 Freestanding libc and Allocator]]

- **Start here · Course:** [Stanford CS107 Assignment 6: Heap Allocator](https://web.stanford.edu/class/archive/cs/cs107/cs107.1236/assign6/index.html) — Follow its progression from bump allocation to implicit and explicit free lists, splitting, coalescing, heap validation, scripted traces, and utilization measurement.
- **Reference · Manual:** [Embed with GNU: libgloss](https://sourceware.org/newlib/libgloss.html) — Use its crt0, linker-script, I/O-hook, and allocation-support guidance to connect startup, BSS/data initialization, stack setup, and the freestanding runtime.
- **Reference · Specification:** [WG14 N2176: C17 Draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2176.pdf) — Use the freestanding-environment, allocation, string, and byte-operation clauses to define contracts and host differential tests.
- **Go deeper · Project:** [musl String Function Sources](https://git.musl-libc.org/cgit/musl/tree/src/string) — After writing your own routines, compare small production implementations of memcpy, memmove, memcmp, strlen, and related functions, especially overlap and byte semantics.

### [[04.04 Ethernet Controller]]

- **Start here · Specification:** [RFC 9542: IANA Considerations and IETF Protocol Usage for IEEE 802 Parameters](https://www.rfc-editor.org/rfc/rfc9542.html) — Use its Ethernet MAC and EtherType layout plus local experimental EtherTypes 0x88B5 and 0x88B6 to build endian-explicit frame fixtures.
- **Reference · Specification:** [IEEE 802.3-2022 Ethernet Standard](https://standards.ieee.org/ieee/802.3/10422/) — Use the MAC clauses as the normative reference for frame fields, permitted sizes, padding, and FCS while keeping the exercise scoped to a small controller model.
- **Reference · Manual:** [Linux Dynamic DMA Mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html) — Use its ownership, DMA-direction, synchronization, and memory-barrier rules when implementing descriptor-ring and packet-buffer lifecycles.
- **Go deeper · Datasheet:** [Intel Ethernet Controller I210 Datasheet](https://www.intel.com/content/www/us/en/content-details/333016/intel-ethernet-controller-i210-datasheet.html) — Study its TX/RX descriptor rings, head and tail registers, completion bits, and interrupt cause/acknowledgement behavior as a concrete comparison for the simulated MMIO device.

### [[04.05 Network Bootloader]]

- **Start here · Specification:** [RFC 1350: The TFTP Protocol](https://www.rfc-editor.org/rfc/rfc1350.html) — Use its compact transfer packet and state model to practice block numbering, duplicate handling, acknowledgement, retransmission, and timeout behavior; document where the course protocol permits reordering.
- **Reference · Manual:** [MCUboot Bootloader Design](https://docs.mcuboot.com/design.html) — Use its image headers, bounded slots, integrity checks, resumable updates, and boot handoff model to design verify-before-commit semantics.
- **Reference · Manual:** [U-Boot Verified Boot](https://docs.u-boot.org/en/latest/usage/fit/verified-boot.html) — Use it to distinguish corruption-detecting hashes from authenticated signatures and to define checked image metadata and handoff conditions.
- **Go deeper · Manual:** [U-Boot Emulation of Network Devices](https://docs.u-boot.org/en/latest/board/emulation/network.html) — Use its emulated-network and TFTP setup patterns to create a sandboxed localhost fixture for loss, duplication, reordering, corruption, and timeout replays.

## 05 — Operating System

### [[05.01 MMU and Page Tables]]

- **Start here · Course:** [xv6: A Simple, Unix-like Teaching Operating System](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf) — Read the page-table chapter before implementing the lab; draw VPN, PPN, and offset decomposition and trace map, unmap, permission, and exec-mapping lifecycles.
- **Go deeper · Course:** [MIT 6.1810 Page Tables Lab](https://pdos.csail.mit.edu/6.1810/2025/labs/pgtbl.html) — Use its PTE inspection and user-mapping exercises as practice before building the reference page walk, TLB, and differential trace harness.
- **Reference · Specification:** [RISC-V Supervisor-Level ISA](https://docs.riscv.org/reference/isa/priv/supervisor.html) — Use the Sv32, PTE, satp, ASID, page-fault, accessed/dirty-bit, and SFENCE.VMA sections for exact walk, permission, and invalidation behavior.

### [[05.02 Unix-like Operating System]]

- **Start here · Course:** [xv6: A Simple, Unix-like Teaching Operating System](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf) — Use the traps, system calls, page tables, processes, scheduling, sleep/wakeup, file descriptors, and file-system chapters as the conceptual spine for the OS simulator.
- **Go deeper · Course:** [MIT 6.1810 System Calls Lab](https://pdos.csail.mit.edu/6.1810/2025/labs/syscall.html) — Use its user stub, trap, dispatch, process-state, tracing, and debugger workflow to practice the complete syscall path before extending your own system.
- **Reference · Specification:** [POSIX.1-2024 fork](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fork.html) — Use it to specify parent and child return values, copied descriptor tables, shared open-file descriptions, independent process lifetimes, and failure cases.
- **Reference · Specification:** [POSIX.1-2024 exec](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html) — Use its preserved and replaced process attributes, argv rules, failure semantics, and success-does-not-return contract to test atomic exec.

### [[05.03 SD Card and Block Device]]

- **Start here · Specification:** [Virtual I/O Device Specification 1.3: Block Device](https://docs.oasis-open.org/virtio/virtio/v1.3/virtio-v1.3.html) — Use the block-device section's sector, operation, data, status, read, write, flush, and completion model as inspiration for the course request/result API.
- **Reference · Specification:** [SD Association Simplified Specifications](https://www.sdcard.org/downloads/pls/) — Use the Physical Layer Simplified Specification's command, response, state, and initialization diagrams to model a small card state machine that rejects data operations before readiness.
- **Reference · Specification:** [POSIX.1-2024 read and pread](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html) — Use positional-read, EOF, zero-length, short-transfer, and interruption rules to define a safe file-backed sector adapter.
- **Go deeper · Manual:** [Linux Fault Injection Infrastructure](https://docs.kernel.org/fault-injection/fault-injection.html) — Use its every-nth failure, block-I/O failure, timeout, and deterministic configuration patterns to design seeded request faults and reproducible replays.

### [[05.04 FAT Filesystem]]

- **Start here · Manual:** [FAT Filesystem](https://elm-chan.org/docs/fat_e.html) — Use its byte diagrams and formulas to derive FAT16 BPB geometry, FAT entries, directory records, cluster chains, and cluster-to-sector translation by hand before coding.
- **Reference · Specification:** [UEFI Specification 2.10: Media Access](https://uefi.org/specs/UEFI/2.10/13_Protocols_Media_Access.html) — Use the FAT12/16/32 BPB and block-I/O sections to validate boot geometry, directory structure, media boundaries, and interoperability assumptions.
- **Reference · Specification:** [ECMA-107: Volume and File Structure of Disk Cartridges for Information Interchange](https://ecma-international.org/publications-and-standards/standards/ecma-107/) — Use its normative 12-bit and 16-bit FAT allocation, defective-space, descriptor, and short-name rules when defining the supported FAT16 profile.
- **Go deeper · Project:** [The Sleuth Kit FAT Documentation](https://wiki.sleuthkit.org/FAT/) — Use its forensic descriptions and tools as an independent oracle for boot sectors, FAT copies, directory entries, deletion markers, cluster chains, and slack-space corruption cases.

### [[05.05 Init Shell and Utilities]]

- **Start here · Course:** [MIT 6.1810 Xv6 and Unix Utilities Lab](https://pdos.csail.mit.edu/6.S081/2025/labs/util.html) — Use the sleep, find, xargs, primes, and pipe exercises to practice small C utilities plus fork, exec, wait, pipe, and correct file-descriptor closure.
- **Reference · Project:** [MIT xv6-riscv](https://github.com/mit-pdos/xv6-riscv) — Study user/init.c, user/sh.c, user/cat.c, user/ls.c, and user/rm.c as compact references for reaping, command execution, redirection, pipelines, and robust I/O loops.
- **Reference · Specification:** [POSIX.1-2024 Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) — Use the token, command, redirection, pipeline, environment, and built-in sections to freeze the shell's deliberately narrow grammar and explicitly list unsupported features.
- **Go deeper · Manual:** [Buildroot User Manual](https://buildroot.org/downloads/manual/manual.html) — Use its init-system discussion to compare PID 1, service startup, and boot sequencing with the course init process and boot transcript.

## 06 — Browser

### [[06.01 TCP Stack]]

- **Start here · Specification:** [RFC 9293: Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293.html) — Use the free current TCP base specification for the state variables, transition model, sequence and acknowledgment rules, receive-window checks, handshake, data transfer, and FIN traces in the workbook.
- **Reference · Specification:** [RFC 6298: Computing TCP's Retransmission Timer](https://www.rfc-editor.org/rfc/rfc6298.html) — Use its timer start, restart, expiry, retransmit-earliest, and exponential-backoff rules to design the simulated-clock loss and lost-ACK tests; full text is free.
- **Go deeper · Paper:** [RFC 1071: Computing the Internet Checksum](https://www.rfc-editor.org/rfc/rfc1071.html) — Use the worked one's-complement arithmetic, odd-byte handling, end-around carry, and byte-order discussion to implement and hand-check checksum fixtures; this is a free implementation memo, not a normative standard.

### [[06.02 Telnet Server]]

- **Start here · Specification:** [RFC 854: Telnet Protocol Specification](https://www.rfc-editor.org/rfc/rfc854.html) — Use the free protocol text to build the streaming IAC command parser, WILL/WONT/DO/DONT refusal behavior, escaped-IAC handling, and CR-LF versus CR-NUL tests across every split boundary.
- **Reference · Manual:** [fork(2) — Linux manual page](https://man7.org/linux/man-pages/man2/fork.2.html) — Use the inherited-file-descriptor and separate-address-space rules to draw parent and session-child ownership and explain why every unowned socket copy must be closed.
- **Reference · Manual:** [dup(2) — Linux manual page](https://man7.org/linux/man-pages/man2/dup.2.html) — Use dup2 semantics to connect a session socket or pipes to child standard input and output while testing aliasing, close ordering, EOF, and failed handoff paths.
- **Go deeper · Manual:** [poll(2) — Linux manual page](https://man7.org/linux/man-pages/man2/poll.2.html) — Use readiness, POLLHUP, error, timeout, and partial-I/O behavior to prevent one slow client from blocking another and to force deterministic concurrent interleavings.

### [[06.03 Dynamic Linking]]

- **Start here · Specification:** [ELF Object File Format, Chapter 8: Dynamic Linking](https://gabi.xinuos.com/elf/08-dynamic.html) — Use PT_INTERP, the dynamic array, DT_NEEDED ordering, breadth-first dependency scope, map-once behavior, GOT/PLT concepts, and relocation-before-control-transfer as the loader's phase contract; full text is free.
- **Reference · Specification:** [ELF Object File Format, Chapter 7: Program Loading](https://gabi.xinuos.com/elf/07-pheader.html) — Use PT_LOAD file-versus-memory ranges, alignment, zero-fill, and segment permission rules to validate mappings and derive final non-writable executable regions.
- **Reference · Specification:** [ELF Object File Format, Chapter 6: Relocation](https://gabi.xinuos.com/elf/06-reloc.html) — Use REL versus RELA, relocation offsets, symbol indices, addends, relative relocation factors, and bounded target writes when implementing the course's documented relocation formulas.
- **Go deeper · Manual:** [Dynamic Linker Environment Variables — The GNU C Library](https://sourceware.org/glibc/manual/latest/html_node/Dynamic-Linker-Environment-Variables.html) — Use LD_DEBUG categories such as libs, reloc, symbols, bindings, and scopes to obtain a real loader trace and compare it with the learner loader's dependency, lookup, and relocation trace.

### [[06.04 Text Web Browser]]

- **Start here · Specification:** [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112.html) — Use the free current HTTP/1.1 message-syntax and body-length rules to implement incremental status/header parsing, Content-Length, chunked framing, connection-close framing, and conflicting-framing rejection.
- **Reference · Specification:** [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) — Use methods, status codes, fields, Content-Length semantics, Location, redirects, and HTTP URI rules to define exactly what the bounded client accepts and follows.
- **Reference · Specification:** [WHATWG HTML Standard: Parsing HTML documents](https://html.spec.whatwg.org/multipage/parsing.html) — Use selected tokenizer states, character references, parse-error behavior, and tree-construction concepts to specify the constrained streaming subset and malformed fixtures without attempting the entire browser algorithm.
- **Go deeper · Specification:** [WHATWG URL Standard](https://url.spec.whatwg.org/) — Use basic parsing, relative-reference resolution, path shortening, serialization, and scheme handling to implement link normalization while explicitly rejecting every scheme outside the course subset.

## 07 — Physical

### [[07.01 JTAG Interface]]

- **Start here · Manual:** [IEEE Std 1149.1 (JTAG) Testability Primer](https://www.ti.com/lit/pdf/ssya002) — Use this free TI primer for the TAP state diagram, capture-shift-update separation, instruction and data registers, BYPASS, IDCODE, bit flow, and hand-written scan transcripts.
- **Reference · Manual:** [OpenOCD User's Guide: JTAG Commands](https://openocd.org/doc-release/html/JTAG-Commands.html) — Use irscan, drscan, pathmove, stable-state names, BYPASS behavior, and explicit end states to compare the simulated navigator with a real JTAG tool's operation model.
- **Go deeper · Specification:** [The RISC-V Debug Specification](https://docs.riscv.org/reference/debug/_attachments/riscv-debug-specification.pdf) — Use its JTAG Debug Transport Module, IDCODE, BYPASS, reset, and error-response material as a concrete modern target when extending transcript and fault-diagnosis tests.
- **Go deeper · Specification:** [IEEE 1149.1-2013: IEEE Standard for Test Access Port and Boundary-Scan Architecture](https://standards.ieee.org/ieee/1149.1/4484/) — Use this as the authoritative published-standard record; the full text requires purchase or subscription, and IEEE marks this edition inactive-reserved while a revision project is active, so the TI and OpenOCD sources are the practical free readings.

### [[07.02 FPGA Board]]

- **Start here · Project:** [Digilent Arty A7-100 Master XDC](https://github.com/Digilent/digilent-xdc/blob/master/Arty-A7-100-Master.xdc) — Use this official supported-board constraint file as the concrete manifest fixture for package pins, I/O standards, clock constraints, UART, storage, Ethernet, and expansion signals; replace it with the matching vendor file if another board is selected.
- **Reference · Manual:** [7 Series FPGAs PCB Design Guide (UG483)](https://docs.amd.com/v/u/en-US/ug483_7Series_PCB) — Use the official vendor guide to review power-distribution networks, rail requirements, decoupling, return paths, stackup, and signal-integrity assumptions behind the manifest and BOM checklist.
- **Reference · Manual:** [7 Series FPGAs SelectIO Resources User Guide (UG471)](https://docs.amd.com/v/u/en-US/ug471_7Series_SelectIO) — Use bank capabilities, VCCO requirements, I/O-standard compatibility, drive, termination, and clock-capable-pin rules to explain every accepted and rejected pin assignment.
- **Go deeper · Manual:** [7 Series FPGAs Configuration User Guide (UG470)](https://docs.amd.com/v/u/en-US/ug470_7Series_Config) — Use configuration modes, startup sequencing, mode pins, PROGRAM_B, INIT_B, DONE, configuration memory, boundary scan, and JTAG access to audit whether the board remains recoverable before application logic works.

### [[07.03 Hardware Bringup]]

- **Start here · Datasheet:** [Digilent Arty A7 Revision E.2 Schematic](https://digilent.com/reference/_media/programmable-logic/arty-a7/arty-a7-e2-sch.pdf) — Use this official board schematic to turn the bring-up ladder into exact rail, ground, clock, reset, configuration, JTAG, UART, DDR3, flash, and Ethernet checkpoints with named test nodes and expected connectivity.
- **Reference · Manual:** [Vivado Design Suite User Guide: Programming and Debugging (UG908)](https://docs.amd.com/r/en-US/ug908-vivado-programming-debugging) — Use the current Hardware Manager, target connection, device programming, debug-probe, and diagnostic flows to identify the JTAG chain, load a known-good bitstream, and save reproducible programming evidence.
- **Reference · Course:** [Vivado Design Suite Tutorial: Programming and Debugging (UG936)](https://docs.amd.com/r/en-US/ug936-vivado-tutorial-programming-debugging) — Use the official ILA and VIO exercises to capture stable internal events, compare logic traces with the simulator, and localize the first semantic divergence without changing several variables at once.
- **Go deeper · Manual:** [Zynq 7000 SoC and 7 Series Devices Memory Interface Solutions User Guide (UG586)](https://docs.amd.com/r/en-US/ug586_7Series_MIS) — Use initialization, calibration-complete, example traffic generator, address mapping, timing-window, and interface-debug material before interpreting walking-bit or address-alias RAM failures.

## Capstone

### [[Capstone - Browser in a Box]]

- **Start here · Project:** [Reproducible Builds Documentation](https://reproducible-builds.org/docs/) — Use the free project guidance to record source revision, toolchain, environment, paths, timestamps, and build inputs so the single capstone command can be reproduced from a fresh checkout.
- **Reference · Specification:** [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112.html) — Use message framing as the transport-to-parser boundary contract when proving that every tested byte split produces the same parsed response and terminal snapshot.
- **Reference · Specification:** [WHATWG HTML Standard: Parsing HTML documents](https://html.spec.whatwg.org/multipage/parsing.html) — Use selected tokenizer and malformed-input rules to design the unclosed-construct fault, record the first divergent token state, and state precisely how the bounded learner subset differs from a production browser.
- **Go deeper · Manual:** [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) — Use a separate host acceptance build with AddressSanitizer to catch out-of-bounds access, use-after-free, double-free, and leaks during the fault campaign; do not treat it as the final static-linked artifact because the documented runtime does not support static linking.

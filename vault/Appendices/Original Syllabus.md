---
id: "appendix-original-syllabus"
title: "Original Syllabus"
section: "appendices"
tags: ["appendix", "source", "syllabus"]
---

# Original Syllabus

This appendix preserves the 24 source blocks from the repository's original outline. It is historical scope, not a claim that every production-scale component fits the original twelve-week estimate. Languages and approximate line counts below are those named by that outline.

## Section 1 — Intro: Cheating our way past the transistor (0.5 weeks)

1. **So about those transistors.** Course overview: explain that FPGAs can be built from transistors and that integrated circuits package collections of transistors reliably. Understand lookup tables and related FPGA resources. Briefly discuss transistor theory, while recognizing that the cumulative projects cannot begin by fabricating one.
2. **Emulation.** Real hardware limits the course's reach. Use a simulator such as Verilator so anyone with a computer can experiment.

## Section 2 — Bringup: What language is hardware coded in? (0.5 weeks)

3. **Blinking an LED — Verilog, about 10 lines.** The first small program: establish the simulator and begin learning Verilog.
4. **Building a UART — Verilog, about 100 lines.** Introduce Verilog through a real UART, introduce memory-mapped I/O, and permit serial semihosting. Build a serial echo test and LED control.

## Section 3 — Processor: What is a processor anyway? (3 weeks)

5. **Coding an assembler — Python, about 500 lines.** Write a straightforward assembler in parallel with the CPU. Teach ARM assembly. Initially emit raw binary files, changing the workflow when the linker exists.
6. **Building an ARM7 CPU — Verilog, about 1,500 lines.** Divide the processor into subchapters, beginning with a simple pipeline and fetch, decode, and execute. Consider available block RAM and whether SRAM is needed. Keep the design simulatable and synthesizable.
7. **Coding a boot ROM — assembly, about 40 lines.** Bake a monitor into the FPGA image so code can be downloaded into RAM over the serial port and small test programs can run.

## Section 4 — Compiler: A “high” level language (3 weeks)

8. **Building a C compiler — Haskell, about 2,000 lines.** Cover compiler fundamentals, write a parser, split the implementation into subchapters, and emit ARM assembly.
9. **Building a linker — Python, about 300 lines.** Produce ELF files and use them for testing with QEMU and semihosting; the source outline suggested this might take a day with a clever implementation.
10. **libc plus malloc — C, about 500 lines.** Supply the subset needed for more complex programs: routines such as `memcpy`, `memset`, and `printf`, but not a complete set of system-call wrappers.
11. **Building an Ethernet controller — Verilog, about 200 lines.** Communicate with a real PHY and design the MMIO interface carefully.
12. **Writing a bootloader — C, about 300 lines.** Write an Ethernet program that boots a kernel over UDP. This was proposed as the first C program, with the aim of avoiding repeated serial downloads and possibly embedding it in the FPGA image.

## Section 5 — Operating System: Software we take for granted (3 weeks)

13. **Building an MMU — Verilog, about 1,000 lines.** Grow toward an ARM9-like design, explain TLBs, possibly add a memory controller, and add initialization to the bootloader.
14. **Building an operating system — C, about 2,500 lines.** Build a Unix-like system with user-space threads and the calls `open`, `read`, `write`, `close`, `fork`, `execve`, `wait`, `sleep`, `exit`, `mmap`, `munmap`, and `mprotect`. Consider a debugging path from `printf` through a possible kernel GDB remote stub. Split the work into subchapters.
15. **Talking to an SD card — Verilog, about 150 lines, plus a driver.** Build the final required hardware controller and its software driver.
16. **FAT — C, about 300 lines.** Implement a real filesystem, with FAT proposed as the simplest option.
17. **init, shell, download, cat, ls, rm — C, about 250 lines.** Create the first user-space programs.

## Section 6 — Browser: Coming online (1 week)

18. **Building a TCP stack — C, about 500 lines.** Likely place it in the kernel, integrate the Ethernet driver, and add networking calls including `send`, `recv`, `bind`, and `connect`.
19. **telnetd, the power of being multiprocess — C, about 50 lines.** Allow multiple Telnet connections; the source describes it as essentially a bind shell.
20. **Space-saving dynamic linking — C, about 300 lines.** Explain that a dynamic linker is a user-space program and extend the linker as required.
21. **So about that Web — C, 500 or more lines.** Build a polished text-based browser using ANSI terminal features, dynamically linked and as capable as desired.

## Section 7 — Physical: Running on real hardware (1 week)

22. **Talking to an FPGA — C, about 200 lines.** Write code for a USB microcontroller that bit-bangs JTAG.
23. **Building an FPGA board.** Design and assemble a board with FPGA BGA reflow, configuration flash, 50 MHz clock, USB JTAG/flasher through a small Cypress USB microcontroller, LEDs, reset, USB-to-serial, USB power, SD card, expansion connector, and Ethernet. Optional additions included host USB, NTSC output, an ISA port, and PS/2. The source proposed toaster-oven reflow with a multimeter thermometer.
24. **Bringup.** Compile and download the Verilog for the board.

## Preservation note

The active course keeps the cumulative transistor-to-browser idea and maps every numbered source block exactly once. [[Scope Decisions]] records where the executable software-first path narrows, reorders, or makes the original hardware ambition optional.

---
title: "Cumulative Notebook Guide"
tags: ["course", "notebooks", "integration", "testing"]
---

# Cumulative Notebook Guide

The C labs test narrow executable contracts. These notebooks test whether those
contracts still compose as the abstraction level rises. Each notebook consumes
JSON evidence produced by an earlier level, runs known-answer and deliberately
broken cases, and emits the next inspectable contract. A later green notebook
therefore depends on the earlier representation and interface decisions.

## Run the tested spine

From the repository root:

```sh
python3 tools/check_notebooks.py
```

The command validates nbformat, module mappings, artifact dependencies,
standard-library-only imports, missing assertions, stored outputs, and then
executes all five notebooks in a temporary directory without network access or
Jupyter dependencies. `make verify` includes this check.

For interactive work, install the optional frontend with
`python3 -m pip install -e '.[notebooks]'`, set
`COURSE_NOTEBOOK_ARTIFACTS=$PWD/notebook-artifacts`, create that directory, and
run the notebooks in order. The generated directory is ignored by Git.

## Cumulative path

| Level | Executable workbook | Earlier evidence reused | New evidence emitted |
|---:|---|---|---|
| 1 | [Bytes, C memory, and ownership](Notebooks/01_bytes_memory_contract.ipynb) | [[00.04 Bytes Bits and Representation]], [[00.05 Pointers Arrays and Strings]], [[00.06 Structs Memory and Ownership]] | signed/unsigned width, byte order, bounds, and ownership contract |
| 2 | [Logic, waveforms, MMIO, and UART](Notebooks/02_logic_uart_trace.ipynb) | Level 1 byte contract plus [[00.08 Digital Logic and State Machines]] and [[01.02 Simulation and Waveforms]] | a checked [[02.02 UART and MMIO]] trace whose framing preserves byte semantics |
| 3 | [Assembler, CPU, boot image, and relocations](Notebooks/03_cpu_toolchain_image.ipynb) | Levels 1–2 encodings and device trace | an assembled machine image executed by a small CPU and checked at relocation boundaries |
| 4 | [Virtual memory, storage, TCP, and browser](Notebooks/04_system_stack_integration.ipynb) | Level 3 machine image | one cross-layer trace through translation, persistent bytes, transport framing, and rendering |
| 5 | [Simulation-first FPGA, JTAG, flash, and LED](Notebooks/05_simulation_first_bringup.ipynb) | Levels 2 and 4 known-good traces | a bring-up report that separates simulated proof from unresolved physical evidence |

Level 5 is the safe bridge to [[realhw Branch Study]]: the historical partial
hardware work supplies questions about constraints, reset, flash framing, and
observability, while this course requires a tested simulation and a written
physical-unknowns ledger before board work.

## Approval rule

For each notebook, predict one result before execution, make one assertion fail
on purpose, localize the earliest wrong representation or state transition,
then restore the passing case. Keep the emitted JSON plus that debugging note.
Notebook execution demonstrates integration; it does not replace the module's
C lab, workbook, reverse-engineering task, or gate explanation.

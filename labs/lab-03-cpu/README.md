# Lab 03B: Fetch, Decode, Execute

Build the executable counterpart to Lab 03A: a small interpreter for the
FTT-16 instruction set. Although the implementation is a software emulator,
its state transition is the same fetch/decode/execute contract used to reason
about a hardware CPU.

## Interface

```text
program WORD [WORD...]
```

Each argument is one instruction word written as exactly four hexadecimal
digits. At most 128 words are accepted. The CPU has sixteen 8-bit registers,
256 bytes of zero-initialized data memory, and a program counter measured in
instruction words. It executes at most 256 instructions.

Use the instruction table from Lab 03A:

- `0x0000`: halt;
- `1 D imm8`: load immediate;
- `2 D S 0`: wrapping add;
- `3 D S 0`: XOR;
- `4 D addr8` / `5 S addr8`: load/store data memory;
- `6 addr12`: absolute jump to a word index;
- `7 N off8`: if `rN` is zero, branch by the signed offset relative to the
  instruction after the branch.

Any reserved encoding, out-of-range PC, or exhausted execution budget is a
runtime error. Runtime errors return status 3; command/input errors return 2.

## Output and example

On halt, print the halt statistics, all registers, and nonzero memory bytes in
ascending address order. Print `memory empty` if every byte is zero.

```console
$ ./program 112a 1205 2120 0000
halted steps=4 pc=3
registers r0=00 r1=2f r2=05 r3=00 r4=00 r5=00 r6=00 r7=00 r8=00 r9=00 r10=00 r11=00 r12=00 r13=00 r14=00 r15=00
memory empty
```

`steps` includes the halt instruction. The halt PC is the index of that halt;
it is not advanced.

## Concepts

- architectural state and the fetch/decode/execute transition;
- opcode/operand extraction with masks and shifts;
- wrapping 8-bit arithmetic;
- instruction address space versus data address space;
- signed PC-relative control flow and execution budgets;
- final-state comparison as a simple differential-testing oracle.

## Rubric

- 35% correct ALU and load/store semantics;
- 30% correct PC, halt, jump, and conditional-branch behavior;
- 20% invalid-encoding and runaway-program handling;
- 15% exact output and warning-free, bounds-safe C17.

## Debug hints

Keep `next_pc` explicit on paper for each instruction. Decode the opcode before
reading fields whose meaning depends on it. For `jz`, sign-extend the low byte
conceptually, add it to `pc + 1`, then validate the result before converting to
an array index. A budget check turns accidental infinite loops into evidence
instead of a hung checker.

## Native C tests

Run `make test` from this lab directory to test the reference solution. Run
`make test SOURCE=/absolute/path/main.c` to test your learner source instead.

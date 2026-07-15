# Lab 01: LUTs, Clocks, and State

Model two pieces of digital hardware in ordinary C: a two-input lookup table
and a clocked wrapping counter. The goal is to make the boundary between
combinational logic (output depends on current inputs) and sequential logic
(output also depends on stored state) concrete.

## Interface

The program has two modes:

```text
program lut MASK
program counter BITS CYCLES
```

`MASK` is an integer from 0 through 15. LUT bit `(a * 2 + b)` is the output for
inputs `a,b`. Thus mask 8 is AND, mask 6 is XOR, and mask 14 is OR. Print all
four input combinations in ascending index order.

`counter` starts at zero, prints its initial state as cycle 0, then increments
on each rising edge. It wraps modulo `2^BITS`. `BITS` is 1 through 8 and
`CYCLES` is 0 through 32.

## Examples

```console
$ ./program lut 8
a=0 b=0 y=0
a=0 b=1 y=0
a=1 b=0 y=0
a=1 b=1 y=1
```

```console
$ ./program counter 2 4
cycle=0 q=0
cycle=1 q=1
cycle=2 q=2
cycle=3 q=3
cycle=4 q=0
```

Invalid commands or ranges print one `error:` line and return status 2.
Decimal and `0x`-prefixed integers are accepted.

## Concepts

- truth-table indexing and LUT configuration bits;
- combinational output versus clocked state;
- masks, shifts, and bounded unsigned arithmetic;
- reset state, rising edges, and rollover;
- why a waveform is just a state trace indexed by time.

## Rubric

- 35% correct LUT indexing and truth-table order;
- 35% correct initial state, edges, and wrapping;
- 15% exact validation and output;
- 15% strict, warning-free C17 without shift or overflow hazards.

## Debug hints

Write the four LUT indexes next to `00`, `01`, `10`, and `11`. For the counter,
calculate the modulus once from the validated width; do not special-case each
width. Cycle 0 is an observation before any edge, not the first increment.

## Native C tests

Run `make test` from this lab directory to compile the solution and exercise
every checked behavior with the native C test executable. Run
`make test SOURCE=/absolute/path/main.c` to test your own implementation.

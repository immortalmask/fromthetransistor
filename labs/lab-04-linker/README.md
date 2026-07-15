# Lab 04B: Apply linker relocations

A linker does not paste text files together. It lays out bytes, assigns symbol
addresses, and patches places that could not be resolved by the assembler. This
lab isolates that last operation.

## Interface

```text
program abs32 PLACE SYMBOL ADDEND
program rel32 PLACE SYMBOL ADDEND
```

Numbers accept C notation (`4096`, `0x1000`). `PLACE` and `SYMBOL` are unsigned
32-bit addresses; `ADDEND` is signed 32-bit. Compute:

- `abs32`: `S + A`
- `rel32`: `S + A - P`

Arithmetic is modulo 2^32, matching a 32-bit relocation field. Print the value
and its little-endian bytes exactly as documented by the examples in the public
tests. Reject an unknown relocation or malformed/out-of-range operand with
status 2.

Before coding, calculate a backwards `rel32` on paper. Keep the mathematical
value separate from byte serialization: linkers repeatedly fail when address
arithmetic, signed interpretation, and target endianness are mixed together.

## Native C tests

Run `make test` from this lab directory to test the reference solution. Run
`make test SOURCE=/absolute/path/main.c` to test your learner source instead.

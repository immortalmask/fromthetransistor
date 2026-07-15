# Lab 03A: A Fixed-Width Assembler

Encode and decode a deliberately small 16-bit instruction set. This is the
first half of an assembler/emulator pair: the words emitted here are accepted
by Lab 03B's CPU.

## Interface

```text
program asm INSTRUCTION [OPERANDS...]
program dis WORD
```

Registers are `r0` through `r15`. Numeric operands accept decimal or a `0x`
prefix. `WORD` is exactly four hexadecimal digits. Successful assembly prints
both the logical word and its two bytes in little-endian memory order.

## Instruction format

| Assembly | Word fields | Meaning |
|---|---|---|
| `halt` | `0x0000` | stop execution |
| `ldi rD IMM8` | `1 D imm8` | load an unsigned immediate |
| `add rD rS` | `2 D S 0` | wrapping 8-bit addition |
| `xor rD rS` | `3 D S 0` | bitwise exclusive-or |
| `load rD ADDR8` | `4 D addr8` | load a data-memory byte |
| `store rS ADDR8` | `5 S addr8` | store a data-memory byte |
| `jmp ADDR12` | `6 addr12` | set the instruction index |
| `jz rN OFFSET8` | `7 N off8` | branch relative to the next word if zero |

`IMM8`/`ADDR8` range from 0 through 255, `ADDR12` from 0 through 4095, and
`OFFSET8` from -128 through 127. The low nibble of `add` and `xor` is reserved
and must be zero.

## Examples

```console
$ ./program asm ldi r2 42
word=0x122a bytes=2a 12
$ ./program asm jz r3 -2
word=0x73fe bytes=fe 73
$ ./program dis 122a
ldi r2, 42
```

Invalid syntax, ranges, registers, encodings, or opcodes produce one `error:`
line and status 2.

## Concepts

- fixed-width instruction fields and opcode dispatch;
- little-endian storage versus the human-readable word;
- signed two's-complement branch displacements;
- strict parsing, reserved bits, and rejecting ambiguous input;
- assembler/disassembler symmetry as a reverse-engineering tool.

## Rubric

- 35% correct encoding of all eight instructions;
- 30% correct decoding, including signed offsets;
- 20% range and reserved-bit validation;
- 15% exact, warning-free, portable C17 output.

## Debug hints

Sketch the word as four hexadecimal nibbles. Build words with unsigned masks
and shifts. For a negative branch offset, reason about its low eight bits, but
validate the signed range before converting. The displayed bytes are low byte
first even though the displayed word reads high nibble first.

## Native C tests

Run `make test` from this lab directory to compile the solution and exercise
every checked behavior with the native C test executable. Run
`make test SOURCE=/absolute/path/main.c` to test your own implementation.

# Lab 00: Bytes and Endianness

Decode a compact binary header of the sort you would meet while reverse
engineering a file format. The lab is deliberately small: the hard part is
being exact about bytes, bit flags, validation, and byte order.

## Interface

Build `main.c` as a C17 program, then pass exactly eight bytes as two-digit
hexadecimal arguments:

```text
program BYTE0 BYTE1 BYTE2 BYTE3 BYTE4 BYTE5 BYTE6 BYTE7
```

The record layout is:

| Offset | Meaning |
|---:|---|
| 0..1 | magic bytes `46 54` (`FT`) |
| 2 | version; only version `01` is supported |
| 3 | flags: bit 0 `compressed`, bit 1 `executable`, bit 2 `debug` |
| 4..5 | unsigned payload length, little-endian |
| 6..7 | unsigned entry address, big-endian |

Upper- or lower-case hexadecimal is accepted. Each argument must contain
exactly two hexadecimal digits. Unknown flag bits are invalid.

## Output and examples

Successful output is one exact line:

```console
$ ./program 46 54 01 05 34 12 20 00
magic=FT version=1 flags=compressed,debug length=4660 entry=0x2000
```

When no flags are set, print `flags=none`. Errors are a single line beginning
with `error:` and exit status 2. Do not print partial decoded output on error.

## Concepts

- bytes versus textual hexadecimal;
- integer promotion and fixed-width unsigned types;
- little-endian versus big-endian decoding;
- bit masks and unknown/reserved bits;
- validating a complete object before trusting its fields.

## Rubric

- 35% exact byte parsing and diagnostics;
- 30% correct mixed-endian decoding;
- 20% flag validation and stable formatting;
- 15% warning-free, readable C17 with no out-of-bounds access.

## Debug hints

Work on paper first: write the contribution of offsets 4 and 5 to the length
as powers of 256. Decode flags with masks rather than equality tests, because
several flags may be set together. Validate both characters before converting
a byte. The checker compares whitespace and letter case exactly.

## Native C tests

Run `make test` from this lab directory to compile the solution and exercise
every checked behavior with the native C test executable. Run
`make test SOURCE=/absolute/path/main.c` to test your own implementation.

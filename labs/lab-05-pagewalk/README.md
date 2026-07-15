# Lab 05A: Page Translation and Protection

Implement one deterministic page-table lookup. The model is intentionally
small enough to trace on paper while preserving the important MMU contract:
split a virtual address, inspect permissions, and either produce a physical
address or a precise fault.

## Interface

```text
program ACCESS VA PTE
```

`ACCESS` is `read`, `write`, or `execute`. `VA` and `PTE` are unsigned 16-bit
integers written in decimal or with a `0x` hexadecimal prefix.

Pages are 256 bytes, so a virtual address has an 8-bit virtual page number and
an 8-bit offset. The single 16-bit PTE has this exact layout:

```text
15                         8 7         3 2 1 0
+---------------------------+-----------+-+-+-+
| physical page number PPN  | reserved  |X|W|P|
+---------------------------+-----------+-+-+-+
```

- `P`: present;
- `W`: writes permitted;
- `X`: instruction fetches permitted;
- bits 7..3: reserved and required to be zero.

A present page is always readable. Translation preserves the low eight offset
bits and replaces the virtual page number with the PTE's physical page number.

## Output and examples

```console
$ ./program read 0x1234 0xab01
vpn=0x12 offset=0x34 ppn=0xab pa=0xab34 access=read
$ ./program write 0x1234 0xab01
fault=write-protection vpn=0x12
```

Translation faults return status 3. Invalid commands, numbers, or reserved PTE
bits print one `error:` line and return status 2.

## Concepts

- page number/offset decomposition;
- PTE bit layouts and fixed-width masking;
- permission checks before address construction;
- the difference between malformed input and an architectural page fault;
- offset preservation as a useful MMU invariant.

## Rubric

- 35% correct VA decomposition and PA construction;
- 35% correct present/write/execute fault priority;
- 15% reserved-bit and numeric validation;
- 15% exact, warning-free, bounds-safe C17.

## Debug hints

With a 256-byte page, division and remainder by 256 are equivalent to taking
the high and low bytes. Check `P` before either access-specific permission.
Never shift an unvalidated signed value. A translated physical address must
have exactly the same low byte as its virtual address.

## Native C tests

Run `make test` from this lab directory to test the reference solution. Run
`make test SOURCE=/absolute/path/main.c` to test your own implementation.

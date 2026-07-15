# Lab 05B: Inspect a FAT Directory Entry

Parse one raw 32-byte FAT directory entry. This is a compact reverse-
engineering exercise: the same bytes can be an end marker, a deleted slot, a
long-filename fragment, or a live 8.3 entry.

## Interface

```text
program HEX64
```

`HEX64` is exactly 64 hexadecimal characters with no separators. Upper- and
lower-case digits are accepted. They represent the entry's 32 bytes in disk
order.

Classification happens in this order:

1. byte 0 is `00`: end marker;
2. byte 0 is `e5`: deleted entry;
3. attribute byte 11 is `0f`: long-filename (LFN) entry;
4. otherwise: an ASCII short-name entry.

For an LFN entry, byte 0 holds sequence bits 0..4 and the `last` flag in bit 6;
byte 13 is the checksum. For a live short entry:

- bytes 0..7 are the space-padded base name;
- bytes 8..10 are the space-padded extension;
- byte 11 is the attribute byte;
- bytes 20..21 are the little-endian high cluster word;
- bytes 26..27 are the little-endian low cluster word;
- bytes 28..31 are the little-endian file size.

This lab deliberately accepts only printable ASCII short names with trailing
space padding.

## Output and example

```console
$ ./program 524541444d4520205458542000000000000000000000000000000500d2040000
kind=short name=README.TXT attr=0x20 cluster=5 size=1234
```

Other classifications print `kind=end`, `kind=deleted`, or:

```text
kind=lfn sequence=N last=yes|no checksum=0xHH
```

Malformed hexadecimal, invalid LFN sequence values, and unsupported short-name
bytes print one `error:` line and exit status 2.

## Concepts

- tagged interpretation of a fixed-size on-disk record;
- sentinel/deleted markers and classification priority;
- 8.3 space padding;
- little-endian 16- and 32-bit reconstruction;
- why FAT32 splits a cluster number across two nonadjacent fields.

## Rubric

- 25% exact 64-character hexadecimal decoding;
- 25% end/deleted/LFN classification;
- 30% short name, cluster, and size decoding;
- 20% exact diagnostics and warning-free, bounds-safe C17.

## Debug hints

Number all 32 bytes before coding. Do classification before attempting to
interpret a short name. Reconstruct little-endian values with unsigned shifts
after promoting each byte. Trim only trailing padding: an ordinary space
followed later by a non-space is malformed in this bounded short-name subset.

## Native C tests

Run `make test` from this lab directory to test the reference solution. Run
`make test SOURCE=/absolute/path/main.c` to test your own implementation.

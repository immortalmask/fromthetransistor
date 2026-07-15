# Lab 02: UART Framing and Status

Implement the byte-level core of an 8N1 UART. This lab turns one byte into the
wire order used by a serial transmitter, validates a received frame, and models
the ready flags an MMIO UART would expose to software.

## Interface

```text
program encode HEXBYTE
program decode FRAME
program echo FRAME
```

`HEXBYTE` is exactly two hexadecimal digits. A `FRAME` is exactly ten binary
digits in time order:

```text
start(0), data bit 0, data bit 1, ... data bit 7, stop(1)
```

UART transmits each byte least-significant bit first. `decode` prints the
received byte and an ASCII character; bytes outside printable ASCII use `.`.
`echo` models firmware observing `RX_READY`, reading the byte, and transmitting
the same byte while `TX_READY` is set.

## Examples

```console
$ ./program encode 41
frame=0100000101
$ ./program decode 0100000101
byte=0x41 ascii=A
$ ./program echo 0100000101
rx=0x41 status=RX_READY|TX_READY tx=0100000101
```

Invalid bytes, frame length/characters, start bits, or stop bits produce one
`error:` line and exit status 2.

## Concepts

- serial versus parallel representation;
- least-significant-bit-first transmission;
- framing and validation before consuming data;
- status bits as the software/hardware contract;
- pure encode/decode functions as testable device-model components.

## Rubric

- 30% exact 8N1 encoding;
- 30% safe decoding and framing checks;
- 20% exact status/ASCII presentation;
- 20% clear, warning-free C17 with fixed-width unsigned data.

## Debug hints

Number frame positions 0 through 9 before writing code. The data bit numbered
`i` belongs at frame position `i + 1`. Decode by setting a result bit rather
than trying to read the displayed string as an ordinary binary integer. Check
the frame length before indexing its start or stop bit.

## Native C tests

Run `make test` from this lab directory to compile the solution and exercise
every checked behavior with the native C test executable. Run
`make test SOURCE=/absolute/path/main.c` to test your own implementation.

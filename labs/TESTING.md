# C lab testing ladder

Every executable lab is an actual C17 program. The checker compiles the
learner's `main.c` for each run and then executes deterministic command-line or
standard-input cases. The compile contract is intentionally strict:

Run `make verify` for the complete baseline. It also proves the starters remain
incomplete and repeats every reference solution with undefined-behavior
instrumentation.

```text
-std=c17 -O2 -Wall -Wextra -Werror -Wpedantic
-Wconversion -Wsign-conversion -Wshadow
```

The reference solutions must pass every case. Each starter must still compile
under that contract but fail at least one behavioral case, so a learner sees a
useful runtime failure rather than being blocked by unrelated scaffold errors.

## Where the tests live

Each lab exposes the contract in two co-located forms:

- `lab.json` is driven by `python3 ftt check` so the CLI can create workspaces,
  record progress, apply resource limits, and report structured results.
- `tests/test.c` is a native C17 black-box suite. It forks the separately
  compiled lab program, supplies arguments or raw stdin bytes, and checks its
  exit status and output. It does not include the solution source or call
  private implementation functions.

Run a single native suite from its lab directory:

```sh
make test
make test SOURCE=/absolute/path/to/your/main.c
```

Run all native suites from the repository root with `make c-tests`. The named
cases, arguments, input bytes, exit codes, and outputs in C and JSON are
generated from one contract and checked for byte-for-byte synchronization, so
both entry points teach the same public behavior.

`python3 ftt start <module-or-lab>` copies the native suite and its Makefile into
the learner workspace. There, `make test` always recompiles `main.c` before
running the cases; no course solution is copied or linked into the workspace.

## Cumulative contracts

| Lab | New C contract under test | Contract reused later |
|---|---|---|
| `lab-00-bytes` | exact-width hexadecimal input, mixed endianness, bit masks, validate-before-decode | UART frames, instruction words, relocation bytes, PTEs and FAT records |
| `lab-01-logic` | LUT addressing, explicit reset state, clock edges and modular wrap | UART state, CPU transitions and the JTAG TAP machine |
| `lab-02-uart` | LSB-first framing, status flags and whole-frame validation before output | device/boot I/O reasoning and the browser's framing-before-payload rule |
| `lab-03-assembler` | all eight opcode encodings, signed fields, reserved bits and little-endian serialization | produces the exact words executed by `lab-03-cpu` |
| `lab-03-cpu` | fetch/decode/execute, wrapping ALU state, memory, taken/not-taken control flow and bounded failure | establishes the machine model consumed by compiler/runtime work |
| `lab-04-compiler` | tokenize/parse/validate before emitting a stack program; precedence and checked arithmetic | the same no-partial-output parser discipline used by the browser |
| `lab-04-linker` | 32-bit modular relocation arithmetic and target-byte serialization | reuses byte order and instruction-address reasoning from sections 00 and 03 |
| `lab-04-allocator` | alignment, non-overlap, capacity subtraction and failure after a successful prefix | supplies the bounds reasoning needed for page tables and bounded parsers |
| `lab-05-pagewalk` | fixed-width address splitting, permission priority, reserved bits and architectural faults | combines masks, addresses and bounds before filesystem/network work |
| `lab-05-fat` | classification before interpretation, padded names, split fields and little-endian disk values | applies the byte parser to a realistic persistent format |
| `lab-06-browser` | HTTP byte counts, duplicate-header rejection, bounded HTML parsing and no partial render | integrates byte, parser, allocator and validation habits |
| `lab-07-jtag` | complete 16-state/32-transition FSM coverage and prevalidated TMS streams | closes the ladder by applying the original logic-state contract to bring-up tooling |

The reset, complete-frame, transfer-boundary and exhaustive TAP cases are also
the simulation-first versions of common real-board bring-up failures. They do
not require an FPGA, USB adapter, network or filesystem image.

## Coverage inventory

The lab specifications currently contain 119 runtime cases:

| Lab | Cases | Notable strengthened boundary |
|---|---:|---|
| `lab-00-bytes` | 8 | uppercase input, asymmetric endian values, magic/version rejection |
| `lab-01-logic` | 9 | reset with zero edges, one-bit wrap, all LUT addresses |
| `lab-02-uart` | 9 | zero byte, nonprintable decode, bad start/nonbinary frames |
| `lab-03-assembler` | 13 | every opcode plus signed/register/address limits and reserved encoding |
| `lab-03-cpu` | 10 | assembler-produced XOR, both branch outcomes, jump and invalid targets |
| `lab-04-compiler` | 11 | negative results, maximum literal, whitespace and incomplete syntax |
| `lab-04-linker` | 9 | extreme addends, wraparound and recognizable little-endian bytes |
| `lab-04-allocator` | 8 | padding to exact capacity and padding-induced exhaustion |
| `lab-05-pagewalk` | 10 | address limits, fault priority and reserved PTE bits |
| `lab-05-fat` | 11 | maximum split fields, LFN boundary and malformed padding |
| `lab-06-browser` | 12 | case folding, duplicate lengths, NUL, unsupported entities and structure |
| `lab-07-jtag` | 9 | one 54-clock walk covers all 32 state/input transitions |

Run the same contract used by the course core:

```console
python3 ftt validate
python3 ftt check --all-solutions
python3 -m unittest discover -s tests -t . -v
make c-tests
```

The unit suite additionally verifies strict flags on every lab, every starter's
intentional failure, complete assembler opcode coverage and complete JTAG
outgoing-edge coverage.

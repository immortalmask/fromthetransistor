# Lab 07: Trace the JTAG TAP Controller

Model the complete IEEE 1149.1 Test Access Port controller as a deterministic
finite-state machine. Each rising TCK edge samples one TMS bit and chooses one
of exactly two outgoing transitions.

## Interface

```text
program TMSBITS
```

`TMSBITS` contains 1 through 64 characters, all `0` or `1`. The controller
starts in `Test-Logic-Reset`. Print the initial state, every sampled bit and
resulting state, then the final state and clock count.

## Complete transition table

| Current state | TMS=0 | TMS=1 |
|---|---|---|
| Test-Logic-Reset | Run-Test/Idle | Test-Logic-Reset |
| Run-Test/Idle | Run-Test/Idle | Select-DR-Scan |
| Select-DR-Scan | Capture-DR | Select-IR-Scan |
| Capture-DR | Shift-DR | Exit1-DR |
| Shift-DR | Shift-DR | Exit1-DR |
| Exit1-DR | Pause-DR | Update-DR |
| Pause-DR | Pause-DR | Exit2-DR |
| Exit2-DR | Shift-DR | Update-DR |
| Update-DR | Run-Test/Idle | Select-DR-Scan |
| Select-IR-Scan | Capture-IR | Test-Logic-Reset |
| Capture-IR | Shift-IR | Exit1-IR |
| Shift-IR | Shift-IR | Exit1-IR |
| Exit1-IR | Pause-IR | Update-IR |
| Pause-IR | Pause-IR | Exit2-IR |
| Exit2-IR | Shift-IR | Update-IR |
| Update-IR | Run-Test/Idle | Select-DR-Scan |

## Example

```console
$ ./program 0100
clock=0 state=Test-Logic-Reset
clock=1 tms=0 state=Run-Test/Idle
clock=2 tms=1 state=Select-DR-Scan
clock=3 tms=0 state=Capture-DR
clock=4 tms=0 state=Shift-DR
final=Shift-DR clocks=4
```

Invalid length, characters, or argument count print one `error:` line and exit
status 2. Validate the entire string before printing a partial trace.

## Concepts

- a finite-state machine represented as data;
- TMS sampling on TCK edges;
- separate instruction-register and data-register scan paths;
- reset sequences and reproducible boundary-scan traces;
- transition coverage as a hardware bringup diagnostic.

## Rubric

- 45% all 32 transitions represented exactly;
- 25% correct initial/edge/final trace semantics;
- 15% complete pre-validation and exact errors;
- 15% table-driven, warning-free C17 without invalid indexing.

## Debug hints

Give every state one enum value, then use a 16-by-2 transition table indexed by
state and TMS. Do not encode the graph as a long collection of special-case
strings. Remember that five consecutive ones keep or return a compliant TAP to
reset regardless of its initial state, while this CLI already starts there.

## Native C tests

Run `make test` from this lab directory to test the reference solution. Run
`make test SOURCE=/absolute/path/main.c` to test your own implementation.

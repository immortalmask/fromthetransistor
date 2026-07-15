---
id: "capstone"
title: "Browser in a Box"
section: "capstone"
tags: ["ftt", "capstone", "integration", "browser"]
---

# Capstone — Browser in a Box

The capstone demonstrates the entire dependency chain without pretending that a
small teaching compiler and CPU already host a production browser. The required
version runs the C browser against an offline fixture server on the host while
reusing the representations and investigation habits built by earlier labs. The
stretch version moves increasingly large pieces onto the course machine.

## Required system

Produce one reproducible command that:

1. validates the course toolchain and builds every learner lab;
2. assembles a small FTT-16 boot image and executes it in the CPU emulator;
3. translates a sample virtual address and decodes a file from a FAT fixture;
4. starts a localhost-only HTTP fixture server on an ephemeral port;
5. fetches a deliberately bounded page, parses status/headers incrementally,
   renders its text and links, and follows one relative link;
6. exits cleanly after the fixture server shuts down;
7. saves a concise linked trace naming the representation at every boundary.

The checked course pieces can be audited together with:

```sh
python3 ftt validate
python3 ftt check --all
```

Your integration command is separate and belongs in learner work. It must work
offline after dependencies are installed.

## Boundary ledger

Fill this before integration:

| producer | representation | consumer | invariant | failure evidence |
|---|---|---|---|---|
| assembler | FTT-16 words | CPU fetch/decode | aligned, known opcode | decode trace |
| page walk | physical address/fault | memory access | permission checked first | fault record |
| FAT reader | bytes + explicit length | file consumer | cluster chain bounded | image offset |
| transport | byte chunks | HTTP parser | no message-boundary assumption | chunk trace |
| HTML tokenizer | tokens | text renderer | progress on every byte | token offset |

Add the interfaces you actually reuse. If two components disagree, repair the
contract rather than adding a conversion whose assumptions are undocumented.

## Fault campaign

Demonstrate diagnosis of at least five injected failures:

- one flipped instruction field;
- one absent or write-protected page;
- one cyclic or out-of-range FAT cluster;
- one HTTP response split at every possible byte boundary;
- one malformed or unclosed HTML construct.

For each, record the first incorrect state, the error reported to the caller,
and the regression test. A crash or hang is not an acceptable error report.

## Required acceptance evidence

- `python3 ftt check --all` passes.
- All required gate exams are at or above their knowledge threshold and their
  practical rubrics have evidence links.
- A fresh checkout plus the learner-work directory can reproduce the capstone.
- The browser never needs the public Internet, root access, or a hardware device.
- Compiler warnings are clean; bounded inputs are enforced at every decoder.
- The final report explains one invariant each for CPU, memory, storage, and
  protocol parsing, plus one limitation that would block production use.

## External sources

Use these for the named task; specifications are lookup material, not cover-to-cover reading.

<!-- ftt:references:start -->
- **Start here · Project:** [Reproducible Builds Documentation](https://reproducible-builds.org/docs/) — Use the free project guidance to record source revision, toolchain, environment, paths, timestamps, and build inputs so the single capstone command can be reproduced from a fresh checkout.
- **Reference · Specification:** [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112.html) — Use message framing as the transport-to-parser boundary contract when proving that every tested byte split produces the same parsed response and terminal snapshot.
- **Reference · Specification:** [WHATWG HTML Standard: Parsing HTML documents](https://html.spec.whatwg.org/multipage/parsing.html) — Use selected tokenizer and malformed-input rules to design the unclosed-construct fault, record the first divergent token state, and state precisely how the bounded learner subset differs from a production browser.
- **Go deeper · Manual:** [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) — Use a separate host acceptance build with AddressSanitizer to catch out-of-bounds access, use-after-free, double-free, and leaks during the fault campaign; do not treat it as the final static-linked artifact because the documented runtime does not support static linking.
<!-- ftt:references:end -->

## Stretch ladder

1. Make the host browser use the learner allocator and byte utilities.
2. Move the fixture page into the learner FAT image.
3. Compile a URL parser or renderer subset with the learner compiler.
4. Run that subset on FTT-16 with a semihosted byte-stream device.
5. Replace semihosting with the simulated NIC and kernel interfaces.
6. Only after the software trace is stable, repeat bringup on an FPGA board.

Each stretch rung must preserve the previous runnable version. The capstone is
about controlled integration and evidence, not maximizing how much code fails
at once.

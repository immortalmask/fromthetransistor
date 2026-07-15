---
title: "Hard Track 06 - Network and Browser in an Adversarial Box"
tags: ["course", "challenge", "hard-track", "stage-06"]
---

# Hard Track 06: Network and Browser in an Adversarial Box

Reverse packet histories, attack TCP and process lifecycles, seal mappings, and fuzz HTTP and HTML before composing a hostile local Web.

**Entry gate:** Complete modules 06.01 through 06.04, gate-06, and the H05 persistent-machine handoff.

**Stage handoff:** A network adversary, TCP corpus, optional sealed loader, browser image, and packet-to-render trace.

Use `python3 ftt challenge start ID` to create an evidence workspace. The
checker replays positive and negative commands and verifies every claimed
artifact by hash; it cannot replace the engineering judgment in the rubric.

### Difficulty ladder

- `*` — focused: one main artifact and a narrow adversarial campaign.
- `**` — cumulative: multiple components, an independent oracle, or substantial fault injection.
- `***` — boss-scale: integrates the stage and produces the handoff consumed later.

## H06.01 · \* · PCAP Archaeology

**Focused · Brutal · 26–39 hours · archaeology**

**Prerequisites:** 06.01, H04.07, H05.08

Reconstruct a missing TCP state transition and bug from packet captures without source access.

**Artifact:** packet decoder, state timeline, hypothesis table, and witness

### Deliverables

- A working packet decoder, state timeline, hypothesis table, and witness with reproducible instructions.
- An independent protocol or parser oracle plus seeded faults.
- A replayable packet-to-process-to-render evidence packet.

### Constraints

- All required networking is loopback or deterministic simulation.
- Protocol and parser queues, states, inputs, and outputs are bounded.
- Content bytes never become unescaped terminal control sequences.

### Adversarial campaign

- retransmission mistaken for new data
- duplicate ACK after reorder
- reset trigger absent from capture

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic protocol and parser checks.
- **A2:** Every adversarial packet or byte split replays without a crash, hang, or leak.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the browser and trace handoff directly.

**Handoff:** The inferred timeline becomes the TCP differential trace.

**Safety:** All services use loopback or simulation; no public bind shell, Internet traffic, TLS claim, or terminal injection.

## H06.02 · \* · Packet Adversary

**Focused · Very Hard · 24–36 hours · adversary**

**Prerequisites:** 06.01, H05.04

Build a deterministic link that loses, duplicates, delays, reorders, corrupts, and fragments packets.

**Artifact:** bounded link simulator, schedule language, and fault corpus

### Deliverables

- A working bounded link simulator, schedule language, and fault corpus with reproducible instructions.
- An independent protocol or parser oracle plus seeded faults.
- A replayable packet-to-process-to-render evidence packet.

### Constraints

- All required networking is loopback or deterministic simulation.
- Protocol and parser queues, states, inputs, and outputs are bounded.
- Content bytes never become unescaped terminal control sequences.

### Adversarial campaign

- every third packet duplicated
- adjacent packets reversed
- fragment dropped until retry

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic protocol and parser checks.
- **A2:** Every adversarial packet or byte split replays without a crash, hang, or leak.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the browser and trace handoff directly.

**Handoff:** The virtual link becomes the required TCP transport.

**Safety:** All services use loopback or simulation; no public bind shell, Internet traffic, TLS claim, or terminal injection.

## H06.03 · \*\* · TCP Wraparound and Close Storm

**Cumulative · Brutal · 44–66 hours · adversary**

**Prerequisites:** H06.01, H06.02

Maintain scoped TCP invariants through wraparound, retransmission, duplicate ACKs, and simultaneous close.

**Artifact:** TCP machine, sequence oracle, schedule corpus, and leak report

### Deliverables

- A working TCP machine, sequence oracle, schedule corpus, and leak report with reproducible instructions.
- An independent protocol or parser oracle plus seeded faults.
- A replayable packet-to-process-to-render evidence packet.

### Constraints

- All required networking is loopback or deterministic simulation.
- Protocol and parser queues, states, inputs, and outputs are bounded.
- Content bytes never become unescaped terminal control sequences.

### Adversarial campaign

- sequence wrap
- simultaneous close
- old duplicate in window

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic protocol and parser checks.
- **A2:** Every adversarial packet or byte split replays without a crash, hang, or leak.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the browser and trace handoff directly.

**Handoff:** The endpoint and corpus become socket services.

**Safety:** All services use loopback or simulation; no public bind shell, Internet traffic, TLS claim, or terminal injection.

## H06.04 · \*\* · Multi-client Telnet Lifecycle

**Cumulative · Brutal · 32–48 hours · integration**

**Prerequisites:** 06.02, H05.05, H06.03

Serve loopback shell sessions while clients disconnect, children exit, and descriptors recycle.

**Artifact:** Telnet service, clients, process trace, and cleanup audit

### Deliverables

- A working Telnet service, clients, process trace, and cleanup audit with reproducible instructions.
- An independent protocol or parser oracle plus seeded faults.
- A replayable packet-to-process-to-render evidence packet.

### Constraints

- All required networking is loopback or deterministic simulation.
- Protocol and parser queues, states, inputs, and outputs are bounded.
- Content bytes never become unescaped terminal control sequences.

### Adversarial campaign

- two clients close together
- child exits with buffered output
- descriptor reused after negotiation failure

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic protocol and parser checks.
- **A2:** Every adversarial packet or byte split replays without a crash, hang, or leak.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the browser and trace handoff directly.

**Handoff:** The lifecycle tests validate sockets and processes.

**Safety:** All services use loopback or simulation; no public bind shell, Internet traffic, TLS claim, or terminal injection.

## H06.05 · \*\* · W-X Dynamic Loader

**Cumulative · Brutal · 38–57 hours · construction**

**Prerequisites:** 06.03, H04.05, H05.01

Map one shared object, resolve approved imports, relocate, and seal permissions without writable-executable overlap.

**Artifact:** userspace loader, import policy, relocation oracle, and mapping trace

### Deliverables

- A working userspace loader, import policy, relocation oracle, and mapping trace with reproducible instructions.
- An independent protocol or parser oracle plus seeded faults.
- A replayable packet-to-process-to-render evidence packet.

### Constraints

- All required networking is loopback or deterministic simulation.
- Protocol and parser queues, states, inputs, and outputs are bounded.
- Content bytes never become unescaped terminal control sequences.

### Adversarial campaign

- unknown import
- relocation overflow
- text remains writable

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic protocol and parser checks.
- **A2:** Every adversarial packet or byte split replays without a crash, hang, or leak.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the browser and trace handoff directly.

**Handoff:** The optional profile passes to the boss but never gates static linking.

**Safety:** All services use loopback or simulation; no public bind shell, Internet traffic, TLS claim, or terminal injection.

## H06.06 · \*\* · HTTP Split-Point Gauntlet

**Cumulative · Brutal · 34–51 hours · adversary**

**Prerequisites:** 06.04, H00.06, H06.03

Prove an incremental HTTP parser returns identical results for every chunking of bounded fixtures.

**Artifact:** stream parser, all-split generator, framing corpus, and oracle

### Deliverables

- A working stream parser, all-split generator, framing corpus, and oracle with reproducible instructions.
- An independent protocol or parser oracle plus seeded faults.
- A replayable packet-to-process-to-render evidence packet.

### Constraints

- All required networking is loopback or deterministic simulation.
- Protocol and parser queues, states, inputs, and outputs are bounded.
- Content bytes never become unescaped terminal control sequences.

### Adversarial campaign

- terminator split
- conflicting length
- body one byte short

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic protocol and parser checks.
- **A2:** Every adversarial packet or byte split replays without a crash, hang, or leak.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the browser and trace handoff directly.

**Handoff:** The parsed-message schema is the HTML layer's only input.

**Safety:** All services use loopback or simulation; no public bind shell, Internet traffic, TLS claim, or terminal injection.

## H06.07 · \*\* · Hostile Markup and Terminal

**Cumulative · Brutal · 38–57 hours · adversary**

**Prerequisites:** 06.04, H06.06

Grammar-fuzz HTML while proving progress, output limits, snapshots, and terminal-control escaping.

**Artifact:** tokenizer-renderer, grammar generator, snapshots, and minimized corpus

### Deliverables

- A working tokenizer-renderer, grammar generator, snapshots, and minimized corpus with reproducible instructions.
- An independent protocol or parser oracle plus seeded faults.
- A replayable packet-to-process-to-render evidence packet.

### Constraints

- All required networking is loopback or deterministic simulation.
- Protocol and parser queues, states, inputs, and outputs are bounded.
- Content bytes never become unescaped terminal control sequences.

### Adversarial campaign

- unclosed nesting
- truncated entity
- escape bytes in text

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic protocol and parser checks.
- **A2:** Every adversarial packet or byte split replays without a crash, hang, or leak.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the browser and trace handoff directly.

**Handoff:** Renderer snapshots become browser evidence.

**Safety:** All services use loopback or simulation; no public bind shell, Internet traffic, TLS claim, or terminal injection.

## H06.08 · \*\*\* · Boss: Hostile Local Web

**Boss-Scale · Brutal · 60–90 hours · boss**

**Prerequisites:** H05.08, H06.03, H06.04, H06.06, H06.07

Fetch FAT-backed pages through packet faults, follow a link, keep Telnet sessions alive, and shut down cleanly.

**Artifact:** browser image, fixture service, integrated trace, snapshots, and audit

### Deliverables

- A working browser image, fixture service, integrated trace, snapshots, and audit with reproducible instructions.
- An independent protocol or parser oracle plus seeded faults.
- A replayable packet-to-process-to-render evidence packet.

### Constraints

- All required networking is loopback or deterministic simulation.
- Protocol and parser queues, states, inputs, and outputs are bounded.
- Content bytes never become unescaped terminal control sequences.

### Adversarial campaign

- loss during linked fetch
- Telnet child exits during render
- malformed second response

### Acceptance evidence

- **A1:** The artifact passes fresh deterministic protocol and parser checks.
- **A2:** Every adversarial packet or byte split replays without a crash, hang, or leak.
- **A3:** Evidence records seed, tools, hashes, first divergence, invariant, and limitation.
- **A4:** The next-stage probe consumes the browser and trace handoff directly.

**Handoff:** Browser image, corpus, and packet-to-render trace pass to physical work.

**Safety:** All services use loopback or simulation; no public bind shell, Internet traffic, TLS claim, or terminal injection.

## Primary references

- [RFC 9293 TCP](https://www.rfc-editor.org/rfc/rfc9293.html) — Define sequence, acknowledgement, retransmission, state, and close invariants.
- [RFC 854 Telnet](https://www.rfc-editor.org/rfc/rfc854.html) — Bound negotiation and explain why the exercise remains loopback-only.
- [RFC 9112 HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112.html) — Specify framing and split-point invariance before HTML parsing.
- [WHATWG HTML parsing](https://html.spec.whatwg.org/multipage/parsing.html) — Select tokenizer behavior and document bounded-subset differences.

Return to [[Challenge Atlas]].

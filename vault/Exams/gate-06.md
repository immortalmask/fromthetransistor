---
id: "gate-06"
title: "Networking and Browser Gate"
section: "exams"
tags: ["exam", "tcp", "http", "browser"]
---

# Networking and Browser Gate

## Purpose

This gate tests whether unreliable packet delivery becomes a safe, bounded, deterministic document pipeline. You must separate transport, HTTP framing, HTML tokenization, layout, and terminal output.

## Objective knowledge

Run `python3 ftt exam gate-06`, answer without packet or parser tooling, and grade using the printed command. For each miss, construct a minimal packet or byte stream that disproves your answer.

## Practical investigation

A local page renders correctly on one run and truncates a link on another when TCP reorders two segments and the HTTP/HTML boundary falls inside a quoted attribute. You receive packet captures, TCP state logs, socket read chunks, HTTP parser state, token trace, and two terminal snapshots.

Before replay, reconstruct both sequence spaces and the expected contiguous byte stream. Then predict HTTP and tokenizer states after each read. Locate the first layer whose output changes when only packet/chunk boundaries change.

Repair that layer and test loss, duplicate overlap, sequence wrap, split header terminator, split chunk size, split entity/tag/attribute, oversized body, terminal escape bytes, and two simultaneous terminal sessions. Plain-text snapshots must be identical across chunkings.

## Rubric

- 20% correct transport and parser-state prediction.
- 30% first boundary-sensitive divergence localized to one layer.
- 25% bounded repair and fragmentation/fault regression suite.
- 15% terminal escaping, resource limits, and session isolation.
- 10% concise end-to-end evidence with intermediate artifacts.

## Safety and limits

Use only the deterministic packet model and localhost fixture server. Do not browse the public Internet, trust Telnet for authentication, render document control bytes, or claim support for TLS, CSS, or JavaScript.

## Completion evidence

Submit objective score, sequence-space reconstruction, chunk-state table, minimized fixture, fixed snapshots at two widths, and resource-limit results.

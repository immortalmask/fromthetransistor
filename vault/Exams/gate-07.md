---
id: "gate-07"
title: "Physical Bringup Gate"
section: "exams"
tags: ["exam", "jtag", "fpga", "bringup", "safety"]
---

# Physical Bringup Gate

## Purpose

This optional gate checks disciplined hardware reasoning: JTAG state, board constraints, dependency-ordered measurements, reproducible artifacts, and explicit stop conditions. The practical can be completed entirely with simulated or recorded evidence.

## Objective knowledge

Run `python3 ftt exam gate-07`, answer before consulting the TAP diagram or bringup checklist, then grade with the printed command. Resolve each miss by tracing state or measurement dependencies.

## Practical investigation

A board report shows acceptable input power, an uncertain core rail, all-ones JTAG IDCODE, and garbled UART after an unrecorded bitstream update. You receive a TAP transcript, board manifest, current/voltage log, build metadata, and logic-analyzer capture.

Do not assume it is safe to continue. Identify missing preflight evidence and write stop/go criteria. Reconstruct the TAP path and bit order, then order the next measurements so each depends only on proven lower layers. Use the simulator or recorded data to test stuck TDO, missing clock, held reset, wrong bank voltage, wrong baud divisor, and stale bitstream hypotheses.

Produce a diagnosis with observation, hypothesis, low-risk experiment, result, and confidence. If using real hardware, obtain experienced review and follow the documented current, voltage, temperature, grounding, and probe limits.

## Rubric

- 25% correct TAP and bit-order reconstruction.
- 25% safe dependency-ordered bringup plan with stop conditions.
- 20% board/power/clock/reset constraints checked before application logic.
- 20% reproducible fault-localization evidence and artifact identity.
- 10% explicit uncertainty and safety discipline.

## Safety and limits

Simulation is sufficient. Never energize hardware with an unknown short, voltage domain, connector orientation, or current limit. Stop immediately on excess current, heat, odor, unstable rails, uncertain ground, or lack of competent supervision. Never probe mains circuitry.

## Completion evidence

Keep objective score, annotated TAP transcript, manifest findings, ordered decision tree, simulated fault results, artifact hashes, and signed-off safety checklist if physical work occurred.

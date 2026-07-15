---
type: "template"
tags: ["ftt", "workbook"]
---

# Workbook — {{module}}

- Date:
- Artifact/commit:

## Prediction before execution

State the expected bytes, trace, output, or state transition before running it.
Name the invariant that makes the prediction plausible.

## Hand trace

| step | input/state | operation | output/next state |
|---:|---|---|---|
| 0 | | | |

## Observations

Record the exact command and the smallest relevant output. Separate observation
from interpretation.

## Debugging record

- Smallest failing input:
- First wrong state:
- Hypotheses ruled out:
- Root cause:
- Regression test added:

## Explain it back

Explain one invariant, one edge condition, and why the abstraction below this
module is sufficient for its caller.

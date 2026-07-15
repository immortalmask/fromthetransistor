# Lab 04A: Compile expressions to stack instructions

Implement the smallest useful compiler pipeline: characters become integer
tokens, recursive-descent functions enforce precedence, and successful parsing
emits postfix instructions for a stack machine.

## Interface

```text
program "EXPRESSION"
```

The language contains non-negative decimal integers, whitespace, `+`, `-`, `*`,
and parentheses. `*` binds tighter than `+` and `-`; binary operators of equal
precedence associate left-to-right. On success print one instruction per line
followed by the evaluated result:

```text
PUSH 2
PUSH 3
PUSH 4
MUL
ADD
RESULT 14
```

Reject malformed input with exit status 2. Do not emit a partial program on an
error: parse into an intermediate instruction buffer, validate the entire input,
then serialize it.

## Work plan

1. Write the grammar `expr := term ((+|-) term)*`, `term := factor (* factor)*`.
2. Hand-trace `12 - 5 - 2` and `(2 + 3) * 4` before coding.
3. Implement a parser cursor and an explicit instruction representation.
4. Add bounds checks before appending an instruction or accumulating a number.
5. Compare emitted order with the order in which the stack machine must execute.

The public checker covers precedence, associativity, parentheses, whitespace,
and one syntax failure. Extend your own tests with large literals and nested
parentheses.

## Native C tests

Run `make test` from this lab directory to test the reference solution. Run
`make test SOURCE=/absolute/path/main.c` to test your learner source instead.

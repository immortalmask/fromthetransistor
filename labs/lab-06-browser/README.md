# Lab 06: Offline HTTP and Text Rendering

Build the parsing core of a text browser without involving a network. The
program receives one complete HTTP response on standard input, validates its
framing, and renders a deliberately bounded HTML subset. Keeping transport out
of the lab makes every parser edge case deterministic.

## Interface

```text
program < response.txt
```

Input is limited to 8192 bytes and may not contain NUL bytes. The accepted HTTP
format is:

- status line `HTTP/1.0 CODE REASON` or `HTTP/1.1 CODE REASON`;
- CRLF line endings and a `\r\n\r\n` header terminator;
- exactly one decimal `Content-Length` header, case-insensitive by name;
- a body whose byte count exactly equals `Content-Length`.

The HTML subset has no attributes. Tag names are case-insensitive. Supported
tags are `html`, `head`, `title`, `body`, `p`, `h1`, `br`, `br/`, `strong`, and
`em`, with closing forms where applicable. `p`, `h1`, and `br` create line
breaks. Text whitespace is collapsed. Supported entities are `&amp;`, `&lt;`,
`&gt;`, `&quot;`, and `&nbsp;`. A single, properly closed `body` is required; the
title is optional.

## Output and example

Given a valid response containing `<title>Demo</title>` and a body with two
paragraphs, output is:

```text
status=200 OK
title=Demo
body:
First paragraph.
Second paragraph.
```

An absent or empty title prints `title=(none)`. Malformed HTTP framing,
length mismatches, unsupported tags/entities, invalid structure, and output
that exceeds the fixed rendering buffers print one `error:` line and return 2.

## Concepts

- byte framing before content parsing;
- bounded reads and length-delimited bodies;
- case-insensitive protocol fields versus exact payload bytes;
- streaming-style tag/entity recognition;
- whitespace normalization and block-versus-inline rendering;
- separating transport, HTTP, parsing, and presentation layers.

## Rubric

- 30% strict, bounded HTTP status/header/body parsing;
- 30% correct title and supported HTML rendering;
- 20% malformed framing, structure, tag, and entity diagnostics;
- 20% exact output and warning-free, memory-safe C17.

## Debug hints

Do not search for HTML until HTTP framing and `Content-Length` agree. Carry an
explicit body length even though valid test bodies are textual. Normalize text
one character at a time, and treat a requested line break as idempotent so
adjacent block tags do not create blank lines. Check capacity before every
append and leave room for a terminator.

## Native C tests

Run `make test` from this lab directory to test the reference solution. Run
`make test SOURCE=/absolute/path/main.c` to test your own implementation.

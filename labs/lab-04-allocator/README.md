# Lab 04C: A bounded aligned arena

Implement the first allocator worth trusting: a fixed 64-byte arena that grants
objects in order and aligns each starting offset to eight bytes. It cannot free;
that simplicity makes ownership and overflow rules visible before free-list
metadata enters the picture.

## Interface

```text
program SIZE [SIZE ...]
```

Each size is a positive decimal integer. For every success, print the requested
size, aligned offset, and exclusive end. Finish with used/capacity. If an object
does not fit, print the successful prefix plus one `oom` line and exit 3. Invalid
input exits 2 without allocation output.

Do not compute `aligned + size` until you know the addition cannot overflow.
The allocator invariant is: every returned range lies inside the arena and no
two returned ranges overlap. Draw the padding for requests `1 8 9` before
running the checker, then extend the lab with reset marks or a free list.

## Native C tests

Run `make test` from this lab directory to test the reference solution. Run
`make test SOURCE=/absolute/path/main.c` to test your learner source instead.

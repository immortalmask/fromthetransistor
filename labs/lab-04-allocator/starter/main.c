#include <stdio.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        fputs("error: expected at least one size\n", stderr);
        return 2;
    }
    (void)argv;
    /* TODO: parse all inputs, then allocate with checked 8-byte alignment. */
    puts("TODO");
    return 0;
}

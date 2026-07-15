#include <stdio.h>

int main(int argc, char **argv)
{
    if (argc != 5) {
        fputs("error: expected TYPE PLACE SYMBOL ADDEND\n", stderr);
        return 2;
    }
    (void)argv;
    /* TODO: parse operands, calculate the relocation, and serialize LE bytes. */
    puts("TODO");
    return 0;
}

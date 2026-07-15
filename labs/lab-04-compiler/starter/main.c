#include <stdio.h>

int main(int argc, char **argv)
{
    if (argc != 2) {
        fputs("error: expected one expression\n", stderr);
        return 2;
    }
    (void)argv;
    /* TODO: tokenize, parse by precedence, buffer instructions, then emit. */
    puts("TODO");
    return 0;
}

#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool parse_bounded(const char *text, unsigned long maximum,
                          unsigned long *result)
{
    char *end = NULL;
    int base = 10;
    unsigned long value;

    if (text[0] == '-') {
        return false;
    }
    if (text[0] == '0' && (text[1] == 'x' || text[1] == 'X')) {
        base = 16;
    }
    errno = 0;
    value = strtoul(text, &end, base);
    if (errno != 0 || end == text || *end != '\0' || value > maximum) {
        return false;
    }
    *result = value;
    return true;
}

static int run_lut(int argc, char **argv)
{
    unsigned long mask;
    unsigned int a;
    unsigned int b;

    if (argc != 3 || !parse_bounded(argv[2], 15UL, &mask)) {
        fprintf(stderr, "error: MASK must be an integer from 0 to 15\n");
        return 2;
    }
    for (a = 0U; a <= 1U; ++a) {
        for (b = 0U; b <= 1U; ++b) {
            unsigned int index = a * 2U + b;
            unsigned long output = (mask >> index) & 1UL;
            printf("a=%u b=%u y=%lu\n", a, b, output);
        }
    }
    return 0;
}

static int run_counter(int argc, char **argv)
{
    unsigned long bits;
    unsigned long cycles;
    unsigned int modulus;
    unsigned int state = 0U;
    unsigned long cycle;

    if (argc != 4 || !parse_bounded(argv[2], 8UL, &bits) || bits == 0UL) {
        fprintf(stderr, "error: BITS must be an integer from 1 to 8\n");
        return 2;
    }
    if (!parse_bounded(argv[3], 32UL, &cycles)) {
        fprintf(stderr, "error: CYCLES must be an integer from 0 to 32\n");
        return 2;
    }
    modulus = 1U << (unsigned int)bits;
    printf("cycle=0 q=0\n");
    for (cycle = 1UL; cycle <= cycles; ++cycle) {
        state = (state + 1U) % modulus;
        printf("cycle=%lu q=%u\n", cycle, state);
    }
    return 0;
}

int main(int argc, char **argv)
{
    if (argc >= 2 && strcmp(argv[1], "lut") == 0) {
        return run_lut(argc, argv);
    }
    if (argc >= 2 && strcmp(argv[1], "counter") == 0) {
        return run_counter(argc, argv);
    }
    fprintf(stderr, "error: expected 'lut MASK' or 'counter BITS CYCLES'\n");
    return 2;
}

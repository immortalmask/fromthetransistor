#include <errno.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

enum { CAPACITY = 64, ALIGNMENT = 8 };

static bool parse_size(const char *text, size_t *size)
{
    char *end = NULL;
    unsigned long long parsed;

    errno = 0;
    parsed = strtoull(text, &end, 10);
    if (errno != 0 || end == text || *end != '\0' || parsed == 0 || parsed > CAPACITY) {
        return false;
    }
    *size = (size_t)parsed;
    return true;
}

static size_t align_up(size_t value)
{
    size_t remainder = value % ALIGNMENT;

    return remainder == 0 ? value : value + (ALIGNMENT - remainder);
}

int main(int argc, char **argv)
{
    size_t sizes[64];
    size_t used = 0;
    int index;

    if (argc < 2 || argc > 65) {
        fputs("error: expected between 1 and 64 sizes\n", stderr);
        return 2;
    }
    for (index = 1; index < argc; ++index) {
        if (!parse_size(argv[index], &sizes[index - 1])) {
            fputs("error: sizes must be positive decimal integers\n", stderr);
            return 2;
        }
    }
    for (index = 1; index < argc; ++index) {
        size_t size = sizes[index - 1];
        size_t offset = align_up(used);

        if (offset > CAPACITY || size > CAPACITY - offset) {
            printf("oom size=%zu used=%zu capacity=%d\n", size, used, CAPACITY);
            return 3;
        }
        used = offset + size;
        printf("alloc size=%zu offset=%zu end=%zu\n", size, offset, used);
    }
    printf("used=%zu capacity=%d\n", used, CAPACITY);
    return 0;
}

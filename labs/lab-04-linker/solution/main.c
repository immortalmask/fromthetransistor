#include <errno.h>
#include <inttypes.h>
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool parse_u32(const char *text, uint32_t *value)
{
    char *end = NULL;
    unsigned long long parsed;

    errno = 0;
    parsed = strtoull(text, &end, 0);
    if (errno != 0 || end == text || *end != '\0' || parsed > UINT32_MAX) {
        return false;
    }
    *value = (uint32_t)parsed;
    return true;
}

static bool parse_i32(const char *text, int32_t *value)
{
    char *end = NULL;
    long long parsed;

    errno = 0;
    parsed = strtoll(text, &end, 0);
    if (errno != 0 || end == text || *end != '\0' || parsed < INT32_MIN || parsed > INT32_MAX) {
        return false;
    }
    *value = (int32_t)parsed;
    return true;
}

int main(int argc, char **argv)
{
    uint32_t place;
    uint32_t symbol;
    uint32_t value;
    int32_t addend;

    if (argc != 5) {
        fputs("error: expected TYPE PLACE SYMBOL ADDEND\n", stderr);
        return 2;
    }
    if (strcmp(argv[1], "abs32") != 0 && strcmp(argv[1], "rel32") != 0) {
        fputs("error: relocation must be abs32 or rel32\n", stderr);
        return 2;
    }
    if (!parse_u32(argv[2], &place) || !parse_u32(argv[3], &symbol)
        || !parse_i32(argv[4], &addend)) {
        fputs("error: malformed or out-of-range operand\n", stderr);
        return 2;
    }
    value = symbol + (uint32_t)addend;
    if (strcmp(argv[1], "rel32") == 0) {
        value -= place;
    }
    printf(
        "value=0x%08" PRIx32 " bytes=%02" PRIx32 " %02" PRIx32 " %02" PRIx32 " %02" PRIx32 "\n",
        value,
        value & UINT32_C(0xff),
        (value >> 8U) & UINT32_C(0xff),
        (value >> 16U) & UINT32_C(0xff),
        (value >> 24U) & UINT32_C(0xff)
    );
    return 0;
}

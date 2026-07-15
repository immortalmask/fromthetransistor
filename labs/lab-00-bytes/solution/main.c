#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { RECORD_SIZE = 8 };

static int hex_value(char character)
{
    if (character >= '0' && character <= '9') {
        return character - '0';
    }
    if (character >= 'a' && character <= 'f') {
        return character - 'a' + 10;
    }
    if (character >= 'A' && character <= 'F') {
        return character - 'A' + 10;
    }
    return -1;
}

static bool parse_byte(const char *text, size_t index, uint8_t *result)
{
    int high;
    int low;

    if (strlen(text) != 2U) {
        fprintf(stderr, "error: byte %zu is not two hexadecimal digits\n", index);
        return false;
    }
    high = hex_value(text[0]);
    low = hex_value(text[1]);
    if (high < 0 || low < 0) {
        fprintf(stderr, "error: byte %zu is not two hexadecimal digits\n", index);
        return false;
    }
    *result = (uint8_t)((unsigned int)high * 16U + (unsigned int)low);
    return true;
}

static void print_flags(uint8_t flags)
{
    bool needs_comma = false;

    fputs("flags=", stdout);
    if (flags == 0U) {
        fputs("none", stdout);
        return;
    }
    if ((flags & UINT8_C(0x01)) != 0U) {
        fputs("compressed", stdout);
        needs_comma = true;
    }
    if ((flags & UINT8_C(0x02)) != 0U) {
        fputs(needs_comma ? ",executable" : "executable", stdout);
        needs_comma = true;
    }
    if ((flags & UINT8_C(0x04)) != 0U) {
        fputs(needs_comma ? ",debug" : "debug", stdout);
    }
}

int main(int argc, char **argv)
{
    uint8_t bytes[RECORD_SIZE];
    uint16_t length;
    uint16_t entry;
    size_t index;

    if (argc != RECORD_SIZE + 1) {
        fprintf(stderr, "error: expected exactly 8 hexadecimal bytes\n");
        return 2;
    }
    for (index = 0U; index < RECORD_SIZE; ++index) {
        if (!parse_byte(argv[index + 1U], index, &bytes[index])) {
            return 2;
        }
    }
    if (bytes[0] != UINT8_C(0x46) || bytes[1] != UINT8_C(0x54)) {
        fprintf(stderr, "error: bad magic (expected 46 54)\n");
        return 2;
    }
    if (bytes[2] != UINT8_C(0x01)) {
        fprintf(stderr, "error: unsupported version %" PRIu8 "\n", bytes[2]);
        return 2;
    }
    if ((bytes[3] & UINT8_C(0xf8)) != 0U) {
        fprintf(stderr, "error: flags contain reserved bits\n");
        return 2;
    }

    length = (uint16_t)((uint16_t)bytes[4] | ((uint16_t)bytes[5] << 8U));
    entry = (uint16_t)(((uint16_t)bytes[6] << 8U) | (uint16_t)bytes[7]);

    printf("magic=FT version=%" PRIu8 " ", bytes[2]);
    print_flags(bytes[3]);
    printf(" length=%" PRIu16 " entry=0x%04" PRIx16 "\n", length, entry);
    return 0;
}

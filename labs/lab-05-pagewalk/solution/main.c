#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum access_kind {
    ACCESS_READ,
    ACCESS_WRITE,
    ACCESS_EXECUTE
};

static int digit_value(char character, unsigned int base)
{
    if (character >= '0' && character <= '9') {
        int value = character - '0';
        return (unsigned int)value < base ? value : -1;
    }
    if (base == 16U && character >= 'a' && character <= 'f') {
        return character - 'a' + 10;
    }
    if (base == 16U && character >= 'A' && character <= 'F') {
        return character - 'A' + 10;
    }
    return -1;
}

static bool parse_u16(const char *text, uint16_t *result)
{
    unsigned int base = 10U;
    unsigned int value = 0U;
    size_t index = 0U;

    if (text[0] == '0' && (text[1] == 'x' || text[1] == 'X')) {
        base = 16U;
        index = 2U;
    }
    if (text[index] == '\0') {
        return false;
    }
    for (; text[index] != '\0'; ++index) {
        int digit = digit_value(text[index], base);
        if (digit < 0) {
            return false;
        }
        value = value * base + (unsigned int)digit;
        if (value > UINT16_MAX) {
            return false;
        }
    }
    *result = (uint16_t)value;
    return true;
}

static bool parse_access(const char *text, enum access_kind *access)
{
    if (strcmp(text, "read") == 0) {
        *access = ACCESS_READ;
        return true;
    }
    if (strcmp(text, "write") == 0) {
        *access = ACCESS_WRITE;
        return true;
    }
    if (strcmp(text, "execute") == 0) {
        *access = ACCESS_EXECUTE;
        return true;
    }
    return false;
}

static const char *access_name(enum access_kind access)
{
    switch (access) {
    case ACCESS_READ:
        return "read";
    case ACCESS_WRITE:
        return "write";
    case ACCESS_EXECUTE:
        return "execute";
    }
    return "invalid";
}

int main(int argc, char **argv)
{
    enum access_kind access;
    uint16_t virtual_address;
    uint16_t pte;
    unsigned int virtual_page;
    unsigned int offset;
    unsigned int physical_page;
    uint16_t physical_address;

    if (argc != 4 || !parse_access(argv[1], &access)) {
        fprintf(stderr, "error: expected ACCESS to be read, write, or execute\n");
        return 2;
    }
    if (!parse_u16(argv[2], &virtual_address)) {
        fprintf(stderr, "error: VA must be an unsigned 16-bit integer\n");
        return 2;
    }
    if (!parse_u16(argv[3], &pte)) {
        fprintf(stderr, "error: PTE must be an unsigned 16-bit integer\n");
        return 2;
    }
    if ((pte & UINT16_C(0x00f8)) != 0U) {
        fprintf(stderr, "error: PTE reserved bits 7..3 must be zero\n");
        return 2;
    }

    virtual_page = (unsigned int)(virtual_address >> 8U);
    offset = (unsigned int)(virtual_address & UINT16_C(0x00ff));
    physical_page = (unsigned int)(pte >> 8U);

    if ((pte & UINT16_C(0x0001)) == 0U) {
        printf("fault=not-present vpn=0x%02x\n", virtual_page);
        return 3;
    }
    if (access == ACCESS_WRITE && (pte & UINT16_C(0x0002)) == 0U) {
        printf("fault=write-protection vpn=0x%02x\n", virtual_page);
        return 3;
    }
    if (access == ACCESS_EXECUTE && (pte & UINT16_C(0x0004)) == 0U) {
        printf("fault=execute-protection vpn=0x%02x\n", virtual_page);
        return 3;
    }

    physical_address = (uint16_t)((uint16_t)(physical_page << 8U) |
                                  (uint16_t)offset);
    printf("vpn=0x%02x offset=0x%02x ppn=0x%02x pa=0x%04x access=%s\n",
           virtual_page, offset, physical_page, (unsigned int)physical_address,
           access_name(access));
    return 0;
}

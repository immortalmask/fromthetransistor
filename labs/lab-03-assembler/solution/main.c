#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

static bool parse_long(const char *text, long minimum, long maximum, long *result)
{
    char *end = NULL;
    const char *magnitude = text;
    int base = 10;
    long value;

    if (*magnitude == '-' || *magnitude == '+') {
        ++magnitude;
    }
    if (magnitude[0] == '0' && (magnitude[1] == 'x' || magnitude[1] == 'X')) {
        base = 16;
    }
    errno = 0;
    value = strtol(text, &end, base);
    if (errno != 0 || end == text || *end != '\0' || value < minimum ||
        value > maximum) {
        return false;
    }
    *result = value;
    return true;
}

static bool parse_register(const char *text, unsigned int *result)
{
    unsigned int value = 0U;
    size_t index;

    if (text[0] != 'r' || text[1] == '\0') {
        return false;
    }
    for (index = 1U; text[index] != '\0'; ++index) {
        if (text[index] < '0' || text[index] > '9') {
            return false;
        }
        value = value * 10U + (unsigned int)(text[index] - '0');
        if (value > 15U) {
            return false;
        }
    }
    *result = value;
    return true;
}

static bool parse_word(const char *text, uint16_t *result)
{
    unsigned int value = 0U;
    size_t index;

    if (strlen(text) != 4U) {
        return false;
    }
    for (index = 0U; index < 4U; ++index) {
        int digit = hex_value(text[index]);
        if (digit < 0) {
            return false;
        }
        value = value * 16U + (unsigned int)digit;
    }
    *result = (uint16_t)value;
    return true;
}

static int emit_word(uint16_t word)
{
    printf("word=0x%04x bytes=%02x %02x\n", (unsigned int)word,
           (unsigned int)(word & UINT16_C(0x00ff)),
           (unsigned int)(word >> 8U));
    return 0;
}

static int assemble(int argc, char **argv)
{
    const char *operation;
    unsigned int destination;
    unsigned int source;
    long value;
    uint16_t word;

    if (argc < 3) {
        goto invalid;
    }
    operation = argv[2];
    if (strcmp(operation, "halt") == 0 && argc == 3) {
        return emit_word(UINT16_C(0x0000));
    }
    if (strcmp(operation, "ldi") == 0 && argc == 5 &&
        parse_register(argv[3], &destination) &&
        parse_long(argv[4], 0L, 255L, &value)) {
        word = (uint16_t)(UINT16_C(0x1000) | (uint16_t)(destination << 8U) |
                          (uint16_t)value);
        return emit_word(word);
    }
    if ((strcmp(operation, "add") == 0 || strcmp(operation, "xor") == 0) &&
        argc == 5 && parse_register(argv[3], &destination) &&
        parse_register(argv[4], &source)) {
        uint16_t opcode = strcmp(operation, "add") == 0 ? UINT16_C(0x2000)
                                                        : UINT16_C(0x3000);
        word = (uint16_t)(opcode | (uint16_t)(destination << 8U) |
                          (uint16_t)(source << 4U));
        return emit_word(word);
    }
    if ((strcmp(operation, "load") == 0 || strcmp(operation, "store") == 0) &&
        argc == 5 && parse_register(argv[3], &destination) &&
        parse_long(argv[4], 0L, 255L, &value)) {
        uint16_t opcode = strcmp(operation, "load") == 0 ? UINT16_C(0x4000)
                                                         : UINT16_C(0x5000);
        word = (uint16_t)(opcode | (uint16_t)(destination << 8U) |
                          (uint16_t)value);
        return emit_word(word);
    }
    if (strcmp(operation, "jmp") == 0 && argc == 4 &&
        parse_long(argv[3], 0L, 4095L, &value)) {
        return emit_word((uint16_t)(UINT16_C(0x6000) | (uint16_t)value));
    }
    if (strcmp(operation, "jz") == 0 && argc == 5 &&
        parse_register(argv[3], &destination) &&
        parse_long(argv[4], -128L, 127L, &value)) {
        uint8_t offset = (uint8_t)(int8_t)value;
        word = (uint16_t)(UINT16_C(0x7000) | (uint16_t)(destination << 8U) |
                          (uint16_t)offset);
        return emit_word(word);
    }

invalid:
    fprintf(stderr, "error: invalid instruction or operands\n");
    return 2;
}

static int disassemble(int argc, char **argv)
{
    uint16_t word;
    unsigned int opcode;
    unsigned int first;
    unsigned int second;
    unsigned int low_byte;

    if (argc != 3 || !parse_word(argv[2], &word)) {
        fprintf(stderr, "error: WORD must be exactly four hexadecimal digits\n");
        return 2;
    }
    opcode = (unsigned int)(word >> 12U);
    first = (unsigned int)((word >> 8U) & UINT16_C(0x000f));
    second = (unsigned int)((word >> 4U) & UINT16_C(0x000f));
    low_byte = (unsigned int)(word & UINT16_C(0x00ff));

    switch (opcode) {
    case 0U:
        if (word == 0U) {
            puts("halt");
            return 0;
        }
        break;
    case 1U:
        printf("ldi r%u, %u\n", first, low_byte);
        return 0;
    case 2U:
    case 3U:
        if ((word & UINT16_C(0x000f)) == 0U) {
            printf("%s r%u, r%u\n", opcode == 2U ? "add" : "xor", first,
                   second);
            return 0;
        }
        break;
    case 4U:
        printf("load r%u, 0x%02x\n", first, low_byte);
        return 0;
    case 5U:
        printf("store r%u, 0x%02x\n", first, low_byte);
        return 0;
    case 6U:
        printf("jmp 0x%03x\n", (unsigned int)(word & UINT16_C(0x0fff)));
        return 0;
    case 7U: {
        int offset = low_byte <= 127U ? (int)low_byte : (int)low_byte - 256;
        printf("jz r%u, %d\n", first, offset);
        return 0;
    }
    default:
        break;
    }
    fprintf(stderr, "error: reserved or unknown instruction encoding\n");
    return 2;
}

int main(int argc, char **argv)
{
    if (argc >= 2 && strcmp(argv[1], "asm") == 0) {
        return assemble(argc, argv);
    }
    if (argc >= 2 && strcmp(argv[1], "dis") == 0) {
        return disassemble(argc, argv);
    }
    fprintf(stderr, "error: expected 'asm' or 'dis'\n");
    return 2;
}

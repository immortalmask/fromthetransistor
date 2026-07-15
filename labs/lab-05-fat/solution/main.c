#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { ENTRY_BYTES = 32, HEX_CHARACTERS = 64 };

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

static bool decode_hex(const char *text, uint8_t bytes[ENTRY_BYTES])
{
    size_t index;

    if (strlen(text) != HEX_CHARACTERS) {
        return false;
    }
    for (index = 0U; index < ENTRY_BYTES; ++index) {
        int high = hex_value(text[index * 2U]);
        int low = hex_value(text[index * 2U + 1U]);
        if (high < 0 || low < 0) {
            return false;
        }
        bytes[index] = (uint8_t)((unsigned int)high * 16U + (unsigned int)low);
    }
    return true;
}

static uint16_t read_le16(const uint8_t bytes[2])
{
    return (uint16_t)((uint16_t)bytes[0] | ((uint16_t)bytes[1] << 8U));
}

static uint32_t read_le32(const uint8_t bytes[4])
{
    return (uint32_t)bytes[0] | ((uint32_t)bytes[1] << 8U) |
           ((uint32_t)bytes[2] << 16U) | ((uint32_t)bytes[3] << 24U);
}

static bool append_name_field(const uint8_t *field, size_t field_size,
                              char *name, size_t *length)
{
    bool padding = false;
    size_t index;

    for (index = 0U; index < field_size; ++index) {
        uint8_t byte = field[index];
        if (byte == UINT8_C(0x20)) {
            padding = true;
            continue;
        }
        if (padding || byte < UINT8_C(0x21) || byte > UINT8_C(0x7e)) {
            return false;
        }
        name[*length] = (char)byte;
        ++*length;
    }
    return true;
}

static bool short_name(const uint8_t bytes[ENTRY_BYTES], char name[13])
{
    size_t length = 0U;
    size_t base_length;

    if (!append_name_field(bytes, 8U, name, &length)) {
        return false;
    }
    base_length = length;
    if (!append_name_field(bytes + 8U, 3U, name, &length)) {
        return false;
    }
    if (base_length == 0U) {
        return false;
    }
    if (length > base_length) {
        size_t index;
        for (index = length; index > base_length; --index) {
            name[index] = name[index - 1U];
        }
        name[base_length] = '.';
        ++length;
    }
    name[length] = '\0';
    return true;
}

int main(int argc, char **argv)
{
    uint8_t bytes[ENTRY_BYTES];
    unsigned int sequence;
    uint32_t cluster;
    uint32_t size;
    char name[13];

    if (argc != 2 || !decode_hex(argc == 2 ? argv[1] : "", bytes)) {
        fprintf(stderr,
                "error: HEX64 must contain exactly 64 hexadecimal characters\n");
        return 2;
    }
    if (bytes[0] == UINT8_C(0x00)) {
        puts("kind=end");
        return 0;
    }
    if (bytes[0] == UINT8_C(0xe5)) {
        puts("kind=deleted");
        return 0;
    }
    if (bytes[11] == UINT8_C(0x0f)) {
        sequence = (unsigned int)(bytes[0] & UINT8_C(0x1f));
        if (sequence == 0U || sequence > 20U ||
            (bytes[0] & UINT8_C(0xa0)) != 0U) {
            fprintf(stderr, "error: invalid LFN sequence byte\n");
            return 2;
        }
        printf("kind=lfn sequence=%u last=%s checksum=0x%02x\n", sequence,
               (bytes[0] & UINT8_C(0x40)) != 0U ? "yes" : "no",
               (unsigned int)bytes[13]);
        return 0;
    }
    if (!short_name(bytes, name)) {
        fprintf(stderr, "error: unsupported or malformed ASCII short name\n");
        return 2;
    }

    cluster = ((uint32_t)read_le16(bytes + 20U) << 16U) |
              (uint32_t)read_le16(bytes + 26U);
    size = read_le32(bytes + 28U);
    printf("kind=short name=%s attr=0x%02x cluster=%" PRIu32 " size=%" PRIu32
           "\n",
           name, (unsigned int)bytes[11], cluster, size);
    return 0;
}

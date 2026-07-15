#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { FRAME_BITS = 10 };

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

static bool parse_hex_byte(const char *text, uint8_t *result)
{
    int high;
    int low;

    if (strlen(text) != 2U) {
        return false;
    }
    high = hex_value(text[0]);
    low = hex_value(text[1]);
    if (high < 0 || low < 0) {
        return false;
    }
    *result = (uint8_t)((unsigned int)high * 16U + (unsigned int)low);
    return true;
}

static void encode_frame(uint8_t byte, char frame[FRAME_BITS + 1])
{
    unsigned int bit;

    frame[0] = '0';
    for (bit = 0U; bit < 8U; ++bit) {
        frame[bit + 1U] = ((byte >> bit) & UINT8_C(1)) != 0U ? '1' : '0';
    }
    frame[9] = '1';
    frame[10] = '\0';
}

static bool decode_frame(const char *frame, uint8_t *result)
{
    unsigned int bit;
    uint8_t byte = 0U;

    if (strlen(frame) != FRAME_BITS) {
        fprintf(stderr, "error: frame must contain exactly ten binary digits\n");
        return false;
    }
    for (bit = 0U; bit < FRAME_BITS; ++bit) {
        if (frame[bit] != '0' && frame[bit] != '1') {
            fprintf(stderr, "error: frame must contain exactly ten binary digits\n");
            return false;
        }
    }
    if (frame[0] != '0') {
        fprintf(stderr, "error: start bit must be 0\n");
        return false;
    }
    if (frame[9] != '1') {
        fprintf(stderr, "error: stop bit must be 1\n");
        return false;
    }
    for (bit = 0U; bit < 8U; ++bit) {
        if (frame[bit + 1U] == '1') {
            byte = (uint8_t)(byte | (uint8_t)(UINT8_C(1) << bit));
        }
    }
    *result = byte;
    return true;
}

static char printable(uint8_t byte)
{
    return byte >= UINT8_C(0x20) && byte <= UINT8_C(0x7e) ? (char)byte : '.';
}

int main(int argc, char **argv)
{
    uint8_t byte;
    char frame[FRAME_BITS + 1];

    if (argc != 3) {
        fprintf(stderr, "error: expected 'encode HEXBYTE', 'decode FRAME', or 'echo FRAME'\n");
        return 2;
    }
    if (strcmp(argv[1], "encode") == 0) {
        if (!parse_hex_byte(argv[2], &byte)) {
            fprintf(stderr, "error: HEXBYTE must be exactly two hexadecimal digits\n");
            return 2;
        }
        encode_frame(byte, frame);
        printf("frame=%s\n", frame);
        return 0;
    }
    if (strcmp(argv[1], "decode") == 0 || strcmp(argv[1], "echo") == 0) {
        if (!decode_frame(argv[2], &byte)) {
            return 2;
        }
        if (strcmp(argv[1], "decode") == 0) {
            printf("byte=0x%02x ascii=%c\n", (unsigned int)byte, printable(byte));
        } else {
            encode_frame(byte, frame);
            printf("rx=0x%02x status=RX_READY|TX_READY tx=%s\n",
                   (unsigned int)byte, frame);
        }
        return 0;
    }
    fprintf(stderr, "error: expected 'encode HEXBYTE', 'decode FRAME', or 'echo FRAME'\n");
    return 2;
}

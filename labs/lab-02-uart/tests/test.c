/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"encode", "41", NULL};
static const char *const ARGS_02[] = {"encode", "ff", NULL};
static const char *const ARGS_03[] = {"decode", "0011111101", NULL};
static const char *const ARGS_04[] = {"echo", "0100000101", NULL};
static const char *const ARGS_05[] = {"decode", "0100000100", NULL};
static const char *const ARGS_06[] = {"encode", "00", NULL};
static const char *const ARGS_07[] = {"decode", "0000000001", NULL};
static const char *const ARGS_08[] = {"decode", "1100000101", NULL};
static const char *const ARGS_09[] = {"echo", "01000x0101", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "encode-ascii-a",
        ARGS_01,
        "",
        0,
        "frame=0100000101\n",
        CTEST_EXACT),
    CTEST_CASE(
        "encode-all-ones",
        ARGS_02,
        "",
        0,
        "frame=0111111111\n",
        CTEST_EXACT),
    CTEST_CASE(
        "decode-printable-byte",
        ARGS_03,
        "",
        0,
        "byte=0x7e ascii=~\n",
        CTEST_EXACT),
    CTEST_CASE(
        "echo-exposes-status",
        ARGS_04,
        "",
        0,
        "rx=0x41 status=RX_READY|TX_READY tx=0100000101\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-bad-stop-bit",
        ARGS_05,
        "",
        2,
        "error: stop bit must be 1\n",
        CTEST_EXACT),
    CTEST_CASE(
        "encode-zero-preserves-start-data-stop-boundaries",
        ARGS_06,
        "",
        0,
        "frame=0000000001\n",
        CTEST_EXACT),
    CTEST_CASE(
        "decode-nonprintable-byte",
        ARGS_07,
        "",
        0,
        "byte=0x00 ascii=.\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-bad-start-bit-before-consuming-data",
        ARGS_08,
        "",
        2,
        "error: start bit must be 0\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-nonbinary-frame-without-partial-echo",
        ARGS_09,
        "",
        2,
        "error: frame must contain exactly ten binary digits\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

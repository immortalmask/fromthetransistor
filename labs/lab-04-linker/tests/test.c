/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"abs32", "0x1000", "0x2000", "4", NULL};
static const char *const ARGS_02[] = {"rel32", "0x1000", "0x1010", "-4", NULL};
static const char *const ARGS_03[] = {"rel32", "0x2000", "0x1ff0", "0", NULL};
static const char *const ARGS_04[] = {"abs32", "0", "0xffffffff", "1", NULL};
static const char *const ARGS_05[] = {"mystery", "0", "0", "0", NULL};
static const char *const ARGS_06[] = {"abs32", "0", "0", "-1", NULL};
static const char *const ARGS_07[] = {"rel32", "0xffffffff", "0", "-2147483648", NULL};
static const char *const ARGS_08[] = {"abs32", "0", "305419896", "0", NULL};
static const char *const ARGS_09[] = {"abs32", "-1", "0", "0", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "absolute-with-addend",
        ARGS_01,
        "",
        0,
        "value=0x00002004 bytes=04 20 00 00\n",
        CTEST_EXACT),
    CTEST_CASE(
        "forward-relative",
        ARGS_02,
        "",
        0,
        "value=0x0000000c bytes=0c 00 00 00\n",
        CTEST_EXACT),
    CTEST_CASE(
        "backward-relative",
        ARGS_03,
        "",
        0,
        "value=0xfffffff0 bytes=f0 ff ff ff\n",
        CTEST_EXACT),
    CTEST_CASE(
        "modulo-wrap",
        ARGS_04,
        "",
        0,
        "value=0x00000000 bytes=00 00 00 00\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-unknown-relocation",
        ARGS_05,
        "",
        2,
        "error: relocation must be abs32 or rel32\n",
        CTEST_EXACT),
    CTEST_CASE(
        "absolute-negative-addend-wraps-modulo-32-bits",
        ARGS_06,
        "",
        0,
        "value=0xffffffff bytes=ff ff ff ff\n",
        CTEST_EXACT),
    CTEST_CASE(
        "relative-extreme-addend-and-place-wrap",
        ARGS_07,
        "",
        0,
        "value=0x80000001 bytes=01 00 00 80\n",
        CTEST_EXACT),
    CTEST_CASE(
        "serialization-reuses-little-endian-byte-contract",
        ARGS_08,
        "",
        0,
        "value=0x12345678 bytes=78 56 34 12\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-negative-unsigned-address",
        ARGS_09,
        "",
        2,
        "error: malformed or out-of-range operand\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

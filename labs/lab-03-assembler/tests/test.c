/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"asm", "halt", NULL};
static const char *const ARGS_02[] = {"asm", "ldi", "r2", "42", NULL};
static const char *const ARGS_03[] = {"asm", "add", "r1", "r2", NULL};
static const char *const ARGS_04[] = {"asm", "jz", "r3", "-2", NULL};
static const char *const ARGS_05[] = {"dis", "122a", NULL};
static const char *const ARGS_06[] = {"dis", "73fe", NULL};
static const char *const ARGS_07[] = {"asm", "xor", "r15", "r0", NULL};
static const char *const ARGS_08[] = {"asm", "load", "r15", "255", NULL};
static const char *const ARGS_09[] = {"asm", "store", "r0", "0", NULL};
static const char *const ARGS_10[] = {"asm", "jmp", "4095", NULL};
static const char *const ARGS_11[] = {"asm", "jz", "r0", "-128", NULL};
static const char *const ARGS_12[] = {"dis", "3f00", NULL};
static const char *const ARGS_13[] = {"dis", "2121", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "assemble-halt",
        ARGS_01,
        "",
        0,
        "word=0x0000 bytes=00 00\n",
        CTEST_EXACT),
    CTEST_CASE(
        "assemble-immediate",
        ARGS_02,
        "",
        0,
        "word=0x122a bytes=2a 12\n",
        CTEST_EXACT),
    CTEST_CASE(
        "assemble-register-operation",
        ARGS_03,
        "",
        0,
        "word=0x2120 bytes=20 21\n",
        CTEST_EXACT),
    CTEST_CASE(
        "assemble-negative-branch",
        ARGS_04,
        "",
        0,
        "word=0x73fe bytes=fe 73\n",
        CTEST_EXACT),
    CTEST_CASE(
        "disassemble-immediate",
        ARGS_05,
        "",
        0,
        "ldi r2, 42\n",
        CTEST_EXACT),
    CTEST_CASE(
        "disassemble-signed-branch",
        ARGS_06,
        "",
        0,
        "jz r3, -2\n",
        CTEST_EXACT),
    CTEST_CASE(
        "assemble-xor-at-register-boundary",
        ARGS_07,
        "",
        0,
        "word=0x3f00 bytes=00 3f\n",
        CTEST_EXACT),
    CTEST_CASE(
        "assemble-load-at-address-boundary",
        ARGS_08,
        "",
        0,
        "word=0x4fff bytes=ff 4f\n",
        CTEST_EXACT),
    CTEST_CASE(
        "assemble-store-zero-address",
        ARGS_09,
        "",
        0,
        "word=0x5000 bytes=00 50\n",
        CTEST_EXACT),
    CTEST_CASE(
        "assemble-maximum-jump-target",
        ARGS_10,
        "",
        0,
        "word=0x6fff bytes=ff 6f\n",
        CTEST_EXACT),
    CTEST_CASE(
        "assemble-minimum-signed-branch",
        ARGS_11,
        "",
        0,
        "word=0x7080 bytes=80 70\n",
        CTEST_EXACT),
    CTEST_CASE(
        "disassemble-xor-round-trip",
        ARGS_12,
        "",
        0,
        "xor r15, r0\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-reserved-alu-low-nibble",
        ARGS_13,
        "",
        2,
        "error: reserved or unknown instruction encoding\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

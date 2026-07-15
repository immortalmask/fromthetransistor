/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"lut", "8", NULL};
static const char *const ARGS_02[] = {"lut", "6", NULL};
static const char *const ARGS_03[] = {"lut", "0xe", NULL};
static const char *const ARGS_04[] = {"counter", "2", "6", NULL};
static const char *const ARGS_05[] = {"counter", "0", "3", NULL};
static const char *const ARGS_06[] = {"lut", "15", NULL};
static const char *const ARGS_07[] = {"counter", "1", "3", NULL};
static const char *const ARGS_08[] = {"counter", "8", "0", NULL};
static const char *const ARGS_09[] = {"lut", "16", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "and-lut",
        ARGS_01,
        "",
        0,
        "a=0 b=0 y=0\na=0 b=1 y=0\na=1 b=0 y=0\na=1 b=1 y=1\n",
        CTEST_EXACT),
    CTEST_CASE(
        "xor-lut",
        ARGS_02,
        "",
        0,
        "a=0 b=0 y=0\na=0 b=1 y=1\na=1 b=0 y=1\na=1 b=1 y=0\n",
        CTEST_EXACT),
    CTEST_CASE(
        "hex-or-lut",
        ARGS_03,
        "",
        0,
        "a=0 b=0 y=0\na=0 b=1 y=1\na=1 b=0 y=1\na=1 b=1 y=1\n",
        CTEST_EXACT),
    CTEST_CASE(
        "two-bit-counter-wraps",
        ARGS_04,
        "",
        0,
        "cycle=0 q=0\ncycle=1 q=1\ncycle=2 q=2\ncycle=3 q=3\ncycle=4 q=0\ncycle=5 q=1\ncycle=6 q=2\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-zero-width",
        ARGS_05,
        "",
        2,
        "error: BITS must be an integer from 1 to 8\n",
        CTEST_EXACT),
    CTEST_CASE(
        "all-ones-lut-covers-every-address",
        ARGS_06,
        "",
        0,
        "a=0 b=0 y=1\na=0 b=1 y=1\na=1 b=0 y=1\na=1 b=1 y=1\n",
        CTEST_EXACT),
    CTEST_CASE(
        "one-bit-counter-wraps-every-other-edge",
        ARGS_07,
        "",
        0,
        "cycle=0 q=0\ncycle=1 q=1\ncycle=2 q=0\ncycle=3 q=1\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reset-state-with-zero-clock-edges",
        ARGS_08,
        "",
        0,
        "cycle=0 q=0\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-mask-outside-four-bit-lut",
        ARGS_09,
        "",
        2,
        "error: MASK must be an integer from 0 to 15\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

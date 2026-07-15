/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"1", "8", "9", NULL};
static const char *const ARGS_02[] = {"8", "8", NULL};
static const char *const ARGS_03[] = {"64", NULL};
static const char *const ARGS_04[] = {"16", "41", "8", NULL};
static const char *const ARGS_05[] = {"0", NULL};
static const char *const ARGS_06[] = {"1", "56", NULL};
static const char *const ARGS_07[] = {"57", "1", NULL};
static const char *const ARGS_08[] = {"65", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "padding-and-mixed-sizes",
        ARGS_01,
        "",
        0,
        "alloc size=1 offset=0 end=1\nalloc size=8 offset=8 end=16\nalloc size=9 offset=16 end=25\nused=25 capacity=64\n",
        CTEST_EXACT),
    CTEST_CASE(
        "already-aligned",
        ARGS_02,
        "",
        0,
        "alloc size=8 offset=0 end=8\nalloc size=8 offset=8 end=16\nused=16 capacity=64\n",
        CTEST_EXACT),
    CTEST_CASE(
        "exact-capacity",
        ARGS_03,
        "",
        0,
        "alloc size=64 offset=0 end=64\nused=64 capacity=64\n",
        CTEST_EXACT),
    CTEST_CASE(
        "out-of-memory-after-prefix",
        ARGS_04,
        "",
        3,
        "alloc size=16 offset=0 end=16\nalloc size=41 offset=16 end=57\noom size=8 used=57 capacity=64\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-zero",
        ARGS_05,
        "",
        2,
        "error: sizes must be positive decimal integers\n",
        CTEST_EXACT),
    CTEST_CASE(
        "padding-then-exact-capacity",
        ARGS_06,
        "",
        0,
        "alloc size=1 offset=0 end=1\nalloc size=56 offset=8 end=64\nused=64 capacity=64\n",
        CTEST_EXACT),
    CTEST_CASE(
        "alignment-padding-causes-out-of-memory",
        ARGS_07,
        "",
        3,
        "alloc size=57 offset=0 end=57\noom size=1 used=57 capacity=64\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-size-above-arena-capacity",
        ARGS_08,
        "",
        2,
        "error: sizes must be positive decimal integers\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

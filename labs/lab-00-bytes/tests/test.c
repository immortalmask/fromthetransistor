/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"46", "54", "01", "05", "34", "12", "20", "00", NULL};
static const char *const ARGS_02[] = {"46", "54", "01", "00", "00", "00", "00", "00", NULL};
static const char *const ARGS_03[] = {"46", "54", "01", "07", "ff", "ff", "ff", "ff", NULL};
static const char *const ARGS_04[] = {"46", "54", "01", "zz", "00", "00", "00", "00", NULL};
static const char *const ARGS_05[] = {"46", "54", "01", "08", "00", "00", "00", "00", NULL};
static const char *const ARGS_06[] = {"46", "54", "01", "02", "01", "80", "AB", "CD", NULL};
static const char *const ARGS_07[] = {"47", "54", "01", "00", "00", "00", "00", "00", NULL};
static const char *const ARGS_08[] = {"46", "54", "02", "00", "00", "00", "00", "00", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "mixed-endian-header",
        ARGS_01,
        "",
        0,
        "magic=FT version=1 flags=compressed,debug length=4660 entry=0x2000\n",
        CTEST_EXACT),
    CTEST_CASE(
        "zero-fields-and-no-flags",
        ARGS_02,
        "",
        0,
        "magic=FT version=1 flags=none length=0 entry=0x0000\n",
        CTEST_EXACT),
    CTEST_CASE(
        "all-flags-and-maximum-fields",
        ARGS_03,
        "",
        0,
        "magic=FT version=1 flags=compressed,executable,debug length=65535 entry=0xffff\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-non-hex-byte",
        ARGS_04,
        "",
        2,
        "error: byte 3 is not two hexadecimal digits\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-reserved-flags",
        ARGS_05,
        "",
        2,
        "error: flags contain reserved bits\n",
        CTEST_EXACT),
    CTEST_CASE(
        "uppercase-hex-and-asymmetric-endianness",
        ARGS_06,
        "",
        0,
        "magic=FT version=1 flags=executable length=32769 entry=0xabcd\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-bad-magic-before-decoding",
        ARGS_07,
        "",
        2,
        "error: bad magic (expected 46 54)\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-unsupported-version",
        ARGS_08,
        "",
        2,
        "error: unsupported version 2\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"524541444d4520205458542000000000000000000000000000000500d2040000", NULL};
static const char *const ARGS_02[] = {"424f4f5420202020202020100000000000000000010000000000020000000000", NULL};
static const char *const ARGS_03[] = {"0000000000000000000000000000000000000000000000000000000000000000", NULL};
static const char *const ARGS_04[] = {"e500000000000000000000000000000000000000000000000000000000000000", NULL};
static const char *const ARGS_05[] = {"41000000000000000000000f00aa000000000000000000000000000000000000", NULL};
static const char *const ARGS_06[] = {"00", NULL};
static const char *const ARGS_07[] = {"524541444D4520205458542000000000000000000000000000000500D2040000", NULL};
static const char *const ARGS_08[] = {"412020202020202042494e200000000000000000ffff00000000ffffffffffff", NULL};
static const char *const ARGS_09[] = {"14000000000000000000000f0055000000000000000000000000000000000000", NULL};
static const char *const ARGS_10[] = {"40000000000000000000000f00aa000000000000000000000000000000000000", NULL};
static const char *const ARGS_11[] = {"4120422020202020545854200000000000000000000000000000000000000000", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "short-file-entry",
        ARGS_01,
        "",
        0,
        "kind=short name=README.TXT attr=0x20 cluster=5 size=1234\n",
        CTEST_EXACT),
    CTEST_CASE(
        "split-cluster-directory",
        ARGS_02,
        "",
        0,
        "kind=short name=BOOT attr=0x10 cluster=65538 size=0\n",
        CTEST_EXACT),
    CTEST_CASE(
        "end-marker",
        ARGS_03,
        "",
        0,
        "kind=end\n",
        CTEST_EXACT),
    CTEST_CASE(
        "deleted-entry",
        ARGS_04,
        "",
        0,
        "kind=deleted\n",
        CTEST_EXACT),
    CTEST_CASE(
        "long-filename-entry",
        ARGS_05,
        "",
        0,
        "kind=lfn sequence=1 last=yes checksum=0xaa\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-wrong-length",
        ARGS_06,
        "",
        2,
        "error: HEX64 must contain exactly 64 hexadecimal characters\n",
        CTEST_EXACT),
    CTEST_CASE(
        "uppercase-hex-input",
        ARGS_07,
        "",
        0,
        "kind=short name=README.TXT attr=0x20 cluster=5 size=1234\n",
        CTEST_EXACT),
    CTEST_CASE(
        "maximum-split-cluster-and-little-endian-size",
        ARGS_08,
        "",
        0,
        "kind=short name=A.BIN attr=0x20 cluster=4294967295 size=4294967295\n",
        CTEST_EXACT),
    CTEST_CASE(
        "maximum-lfn-sequence-without-last-flag",
        ARGS_09,
        "",
        0,
        "kind=lfn sequence=20 last=no checksum=0x55\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-zero-lfn-sequence-even-with-last-flag",
        ARGS_10,
        "",
        2,
        "error: invalid LFN sequence byte\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-internal-short-name-padding",
        ARGS_11,
        "",
        2,
        "error: unsupported or malformed ASCII short name\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"read", "0x1234", "0xab01", NULL};
static const char *const ARGS_02[] = {"write", "0x00ff", "0x4203", NULL};
static const char *const ARGS_03[] = {"execute", "65535", "0x7f05", NULL};
static const char *const ARGS_04[] = {"read", "0x1234", "0xab00", NULL};
static const char *const ARGS_05[] = {"write", "0x1234", "0xab01", NULL};
static const char *const ARGS_06[] = {"execute", "0x1234", "0xab03", NULL};
static const char *const ARGS_07[] = {"read", "0", "0xff07", NULL};
static const char *const ARGS_08[] = {"write", "0x12fe", "0xab06", NULL};
static const char *const ARGS_09[] = {"read", "0x1234", "0xab09", NULL};
static const char *const ARGS_10[] = {"execute", "65536", "0x0005", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "read-present-page",
        ARGS_01,
        "",
        0,
        "vpn=0x12 offset=0x34 ppn=0xab pa=0xab34 access=read\n",
        CTEST_EXACT),
    CTEST_CASE(
        "write-permitted",
        ARGS_02,
        "",
        0,
        "vpn=0x00 offset=0xff ppn=0x42 pa=0x42ff access=write\n",
        CTEST_EXACT),
    CTEST_CASE(
        "execute-permitted",
        ARGS_03,
        "",
        0,
        "vpn=0xff offset=0xff ppn=0x7f pa=0x7fff access=execute\n",
        CTEST_EXACT),
    CTEST_CASE(
        "not-present-fault",
        ARGS_04,
        "",
        3,
        "fault=not-present vpn=0x12\n",
        CTEST_EXACT),
    CTEST_CASE(
        "write-protection-fault",
        ARGS_05,
        "",
        3,
        "fault=write-protection vpn=0x12\n",
        CTEST_EXACT),
    CTEST_CASE(
        "execute-protection-fault",
        ARGS_06,
        "",
        3,
        "fault=execute-protection vpn=0x12\n",
        CTEST_EXACT),
    CTEST_CASE(
        "zero-virtual-address-to-highest-physical-page",
        ARGS_07,
        "",
        0,
        "vpn=0x00 offset=0x00 ppn=0xff pa=0xff00 access=read\n",
        CTEST_EXACT),
    CTEST_CASE(
        "not-present-fault-has-permission-priority",
        ARGS_08,
        "",
        3,
        "fault=not-present vpn=0x12\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-reserved-pte-bit-before-translation",
        ARGS_09,
        "",
        2,
        "error: PTE reserved bits 7..3 must be zero\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-virtual-address-overflow",
        ARGS_10,
        "",
        2,
        "error: VA must be an unsigned 16-bit integer\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"0000", NULL};
static const char *const ARGS_02[] = {"11fe", "1205", "2120", "0000", NULL};
static const char *const ARGS_03[] = {"11ab", "5110", "4210", "0000", NULL};
static const char *const ARGS_04[] = {"1100", "7101", "122a", "1207", "0000", NULL};
static const char *const ARGS_05[] = {"6000", NULL};
static const char *const ARGS_06[] = {"11aa", "1255", "3120", "0000", NULL};
static const char *const ARGS_07[] = {"1101", "7101", "122a", "0000", NULL};
static const char *const ARGS_08[] = {"6002", "11ff", "0000", NULL};
static const char *const ARGS_09[] = {"2121", NULL};
static const char *const ARGS_10[] = {"70fe", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "halt-from-reset",
        ARGS_01,
        "",
        0,
        "halted steps=1 pc=0\nregisters r0=00 r1=00 r2=00 r3=00 r4=00 r5=00 r6=00 r7=00 r8=00 r9=00 r10=00 r11=00 r12=00 r13=00 r14=00 r15=00\nmemory empty\n",
        CTEST_EXACT),
    CTEST_CASE(
        "wrapping-addition",
        ARGS_02,
        "",
        0,
        "halted steps=4 pc=3\nregisters r0=00 r1=03 r2=05 r3=00 r4=00 r5=00 r6=00 r7=00 r8=00 r9=00 r10=00 r11=00 r12=00 r13=00 r14=00 r15=00\nmemory empty\n",
        CTEST_EXACT),
    CTEST_CASE(
        "store-then-load",
        ARGS_03,
        "",
        0,
        "halted steps=4 pc=3\nregisters r0=00 r1=ab r2=ab r3=00 r4=00 r5=00 r6=00 r7=00 r8=00 r9=00 r10=00 r11=00 r12=00 r13=00 r14=00 r15=00\nmemory 10=ab\n",
        CTEST_EXACT),
    CTEST_CASE(
        "taken-relative-branch",
        ARGS_04,
        "",
        0,
        "halted steps=4 pc=4\nregisters r0=00 r1=00 r2=07 r3=00 r4=00 r5=00 r6=00 r7=00 r8=00 r9=00 r10=00 r11=00 r12=00 r13=00 r14=00 r15=00\nmemory empty\n",
        CTEST_EXACT),
    CTEST_CASE(
        "execution-budget-stops-loop",
        ARGS_05,
        "",
        3,
        "error: execution budget exceeded after 256 steps\n",
        CTEST_EXACT),
    CTEST_CASE(
        "executes-assembler-xor-encoding",
        ARGS_06,
        "",
        0,
        "halted steps=4 pc=3\nregisters r0=00 r1=ff r2=55 r3=00 r4=00 r5=00 r6=00 r7=00 r8=00 r9=00 r10=00 r11=00 r12=00 r13=00 r14=00 r15=00\nmemory empty\n",
        CTEST_EXACT),
    CTEST_CASE(
        "nonzero-register-does-not-take-branch",
        ARGS_07,
        "",
        0,
        "halted steps=4 pc=3\nregisters r0=00 r1=01 r2=2a r3=00 r4=00 r5=00 r6=00 r7=00 r8=00 r9=00 r10=00 r11=00 r12=00 r13=00 r14=00 r15=00\nmemory empty\n",
        CTEST_EXACT),
    CTEST_CASE(
        "absolute-jump-skips-instruction",
        ARGS_08,
        "",
        0,
        "halted steps=2 pc=2\nregisters r0=00 r1=00 r2=00 r3=00 r4=00 r5=00 r6=00 r7=00 r8=00 r9=00 r10=00 r11=00 r12=00 r13=00 r14=00 r15=00\nmemory empty\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-reserved-encoding-emitted-by-no-valid-assembler-input",
        ARGS_09,
        "",
        3,
        "error: invalid instruction 0x2121 at pc 0\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-negative-relative-branch-target",
        ARGS_10,
        "",
        3,
        "error: branch target -1 is outside program\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

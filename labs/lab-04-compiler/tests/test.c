/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"2+3*4", NULL};
static const char *const ARGS_02[] = {"(2+3)*4", NULL};
static const char *const ARGS_03[] = {"12 - 5 - 2", NULL};
static const char *const ARGS_04[] = {"7*(8-3)+1", NULL};
static const char *const ARGS_05[] = {"2+", NULL};
static const char *const ARGS_06[] = {"9223372036854775807+1", NULL};
static const char *const ARGS_07[] = {"2-5*3", NULL};
static const char *const ARGS_08[] = {"9223372036854775807*0", NULL};
static const char *const ARGS_09[] = {" ( 2 + 3 ) * 4 ", NULL};
static const char *const ARGS_10[] = {"1 2", NULL};
static const char *const ARGS_11[] = {"(1+2", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "multiplication-precedence",
        ARGS_01,
        "",
        0,
        "PUSH 2\nPUSH 3\nPUSH 4\nMUL\nADD\nRESULT 14\n",
        CTEST_EXACT),
    CTEST_CASE(
        "parentheses-override-precedence",
        ARGS_02,
        "",
        0,
        "PUSH 2\nPUSH 3\nADD\nPUSH 4\nMUL\nRESULT 20\n",
        CTEST_EXACT),
    CTEST_CASE(
        "left-associative-subtraction",
        ARGS_03,
        "",
        0,
        "PUSH 12\nPUSH 5\nSUB\nPUSH 2\nSUB\nRESULT 5\n",
        CTEST_EXACT),
    CTEST_CASE(
        "nested-expression",
        ARGS_04,
        "",
        0,
        "PUSH 7\nPUSH 8\nPUSH 3\nSUB\nMUL\nPUSH 1\nADD\nRESULT 36\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-missing-operand",
        ARGS_05,
        "",
        2,
        "error: expected integer or '('\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-arithmetic-overflow",
        ARGS_06,
        "",
        2,
        "error: arithmetic overflow\n",
        CTEST_EXACT),
    CTEST_CASE(
        "negative-result-after-precedence",
        ARGS_07,
        "",
        0,
        "PUSH 2\nPUSH 5\nPUSH 3\nMUL\nSUB\nRESULT -13\n",
        CTEST_EXACT),
    CTEST_CASE(
        "maximum-literal-times-zero-does-not-overflow",
        ARGS_08,
        "",
        0,
        "PUSH 9223372036854775807\nPUSH 0\nMUL\nRESULT 0\n",
        CTEST_EXACT),
    CTEST_CASE(
        "whitespace-around-nested-expression",
        ARGS_09,
        "",
        0,
        "PUSH 2\nPUSH 3\nADD\nPUSH 4\nMUL\nRESULT 20\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-adjacent-literals-without-operator",
        ARGS_10,
        "",
        2,
        "error: unexpected trailing input\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-unclosed-parenthesis-without-partial-program",
        ARGS_11,
        "",
        2,
        "error: expected ')'\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

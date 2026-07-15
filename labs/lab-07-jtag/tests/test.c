/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {"0", NULL};
static const char *const ARGS_02[] = {"11111", NULL};
static const char *const ARGS_03[] = {"0100", NULL};
static const char *const ARGS_04[] = {"01100", NULL};
static const char *const ARGS_05[] = {"0101011", NULL};
static const char *const ARGS_06[] = {"01x", NULL};
static const char *const ARGS_07[] = {"001000100101101100010010110101111110110111010111101011", NULL};
static const char *const ARGS_08[] = {"", NULL};
static const char *const ARGS_09[] = {"00000000000000000000000000000000000000000000000000000000000000000", NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "leave-reset",
        ARGS_01,
        "",
        0,
        "clock=0 state=Test-Logic-Reset\nclock=1 tms=0 state=Run-Test/Idle\nfinal=Run-Test/Idle clocks=1\n",
        CTEST_EXACT),
    CTEST_CASE(
        "ones-hold-reset",
        ARGS_02,
        "",
        0,
        "clock=0 state=Test-Logic-Reset\nclock=1 tms=1 state=Test-Logic-Reset\nclock=2 tms=1 state=Test-Logic-Reset\nclock=3 tms=1 state=Test-Logic-Reset\nclock=4 tms=1 state=Test-Logic-Reset\nclock=5 tms=1 state=Test-Logic-Reset\nfinal=Test-Logic-Reset clocks=5\n",
        CTEST_EXACT),
    CTEST_CASE(
        "enter-shift-dr",
        ARGS_03,
        "",
        0,
        "clock=0 state=Test-Logic-Reset\nclock=1 tms=0 state=Run-Test/Idle\nclock=2 tms=1 state=Select-DR-Scan\nclock=3 tms=0 state=Capture-DR\nclock=4 tms=0 state=Shift-DR\nfinal=Shift-DR clocks=4\n",
        CTEST_EXACT),
    CTEST_CASE(
        "enter-shift-ir",
        ARGS_04,
        "",
        0,
        "clock=0 state=Test-Logic-Reset\nclock=1 tms=0 state=Run-Test/Idle\nclock=2 tms=1 state=Select-DR-Scan\nclock=3 tms=1 state=Select-IR-Scan\nclock=4 tms=0 state=Capture-IR\nclock=5 tms=0 state=Shift-IR\nfinal=Shift-IR clocks=5\n",
        CTEST_EXACT),
    CTEST_CASE(
        "pause-exit-and-update-dr",
        ARGS_05,
        "",
        0,
        "clock=0 state=Test-Logic-Reset\nclock=1 tms=0 state=Run-Test/Idle\nclock=2 tms=1 state=Select-DR-Scan\nclock=3 tms=0 state=Capture-DR\nclock=4 tms=1 state=Exit1-DR\nclock=5 tms=0 state=Pause-DR\nclock=6 tms=1 state=Exit2-DR\nclock=7 tms=1 state=Update-DR\nfinal=Update-DR clocks=7\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-non-binary-input",
        ARGS_06,
        "",
        2,
        "error: TMSBITS must contain 1 to 64 binary digits\n",
        CTEST_EXACT),
    CTEST_CASE(
        "all-32-tap-transitions",
        ARGS_07,
        "",
        0,
        "clock=0 state=Test-Logic-Reset\nclock=1 tms=0 state=Run-Test/Idle\nclock=2 tms=0 state=Run-Test/Idle\nclock=3 tms=1 state=Select-DR-Scan\nclock=4 tms=0 state=Capture-DR\nclock=5 tms=0 state=Shift-DR\nclock=6 tms=0 state=Shift-DR\nclock=7 tms=1 state=Exit1-DR\nclock=8 tms=0 state=Pause-DR\nclock=9 tms=0 state=Pause-DR\nclock=10 tms=1 state=Exit2-DR\nclock=11 tms=0 state=Shift-DR\nclock=12 tms=1 state=Exit1-DR\nclock=13 tms=1 state=Update-DR\nclock=14 tms=0 state=Run-Test/Idle\nclock=15 tms=1 state=Select-DR-Scan\nclock=16 tms=1 state=Select-IR-Scan\nclock=17 tms=0 state=Capture-IR\nclock=18 tms=0 state=Shift-IR\nclock=19 tms=0 state=Shift-IR\nclock=20 tms=1 state=Exit1-IR\nclock=21 tms=0 state=Pause-IR\nclock=22 tms=0 state=Pause-IR\nclock=23 tms=1 state=Exit2-IR\nclock=24 tms=0 state=Shift-IR\nclock=25 tms=1 state=Exit1-IR\nclock=26 tms=1 state=Update-IR\nclock=27 tms=0 state=Run-Test/Idle\nclock=28 tms=1 state=Select-DR-Scan\nclock=29 tms=0 state=Capture-DR\nclock=30 tms=1 state=Exit1-DR\nclock=31 tms=1 state=Update-DR\nclock=32 tms=1 state=Select-DR-Scan\nclock=33 tms=1 state=Select-IR-Scan\nclock=34 tms=1 state=Test-Logic-Reset\nclock=35 tms=1 state=Test-Logic-Reset\nclock=36 tms=0 state=Run-Test/Idle\nclock=37 tms=1 state=Select-DR-Scan\nclock=38 tms=1 state=Select-IR-Scan\nclock=39 tms=0 state=Capture-IR\nclock=40 tms=1 state=Exit1-IR\nclock=41 tms=1 state=Update-IR\nclock=42 tms=1 state=Select-DR-Scan\nclock=43 tms=0 state=Capture-DR\nclock=44 tms=1 state=Exit1-DR\nclock=45 tms=0 state=Pause-DR\nclock=46 tms=1 state=Exit2-DR\nclock=47 tms=1 state=Update-DR\nclock=48 tms=1 state=Select-DR-Scan\nclock=49 tms=1 state=Select-IR-Scan\nclock=50 tms=0 state=Capture-IR\nclock=51 tms=1 state=Exit1-IR\nclock=52 tms=0 state=Pause-IR\nclock=53 tms=1 state=Exit2-IR\nclock=54 tms=1 state=Update-IR\nfinal=Update-IR clocks=54\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-empty-tms-stream-before-trace",
        ARGS_08,
        "",
        2,
        "error: TMSBITS must contain 1 to 64 binary digits\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-65-clock-stream-before-trace",
        ARGS_09,
        "",
        2,
        "error: TMSBITS must contain 1 to 64 binary digits\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

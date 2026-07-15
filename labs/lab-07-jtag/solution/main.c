#include <stddef.h>
#include <stdio.h>
#include <string.h>

enum tap_state {
    TEST_LOGIC_RESET,
    RUN_TEST_IDLE,
    SELECT_DR_SCAN,
    CAPTURE_DR,
    SHIFT_DR,
    EXIT1_DR,
    PAUSE_DR,
    EXIT2_DR,
    UPDATE_DR,
    SELECT_IR_SCAN,
    CAPTURE_IR,
    SHIFT_IR,
    EXIT1_IR,
    PAUSE_IR,
    EXIT2_IR,
    UPDATE_IR,
    TAP_STATE_COUNT
};

static const char *const state_names[TAP_STATE_COUNT] = {
    "Test-Logic-Reset", "Run-Test/Idle", "Select-DR-Scan", "Capture-DR",
    "Shift-DR",         "Exit1-DR",      "Pause-DR",       "Exit2-DR",
    "Update-DR",        "Select-IR-Scan", "Capture-IR",     "Shift-IR",
    "Exit1-IR",         "Pause-IR",       "Exit2-IR",       "Update-IR"
};

static const enum tap_state transitions[TAP_STATE_COUNT][2] = {
    [TEST_LOGIC_RESET] = {RUN_TEST_IDLE, TEST_LOGIC_RESET},
    [RUN_TEST_IDLE] = {RUN_TEST_IDLE, SELECT_DR_SCAN},
    [SELECT_DR_SCAN] = {CAPTURE_DR, SELECT_IR_SCAN},
    [CAPTURE_DR] = {SHIFT_DR, EXIT1_DR},
    [SHIFT_DR] = {SHIFT_DR, EXIT1_DR},
    [EXIT1_DR] = {PAUSE_DR, UPDATE_DR},
    [PAUSE_DR] = {PAUSE_DR, EXIT2_DR},
    [EXIT2_DR] = {SHIFT_DR, UPDATE_DR},
    [UPDATE_DR] = {RUN_TEST_IDLE, SELECT_DR_SCAN},
    [SELECT_IR_SCAN] = {CAPTURE_IR, TEST_LOGIC_RESET},
    [CAPTURE_IR] = {SHIFT_IR, EXIT1_IR},
    [SHIFT_IR] = {SHIFT_IR, EXIT1_IR},
    [EXIT1_IR] = {PAUSE_IR, UPDATE_IR},
    [PAUSE_IR] = {PAUSE_IR, EXIT2_IR},
    [EXIT2_IR] = {SHIFT_IR, UPDATE_IR},
    [UPDATE_IR] = {RUN_TEST_IDLE, SELECT_DR_SCAN}
};

int main(int argc, char **argv)
{
    enum tap_state state = TEST_LOGIC_RESET;
    const char *bits;
    size_t length;
    size_t index;

    if (argc != 2) {
        fprintf(stderr, "error: TMSBITS must contain 1 to 64 binary digits\n");
        return 2;
    }
    bits = argv[1];
    length = strlen(bits);
    if (length == 0U || length > 64U) {
        fprintf(stderr, "error: TMSBITS must contain 1 to 64 binary digits\n");
        return 2;
    }
    for (index = 0U; index < length; ++index) {
        if (bits[index] != '0' && bits[index] != '1') {
            fprintf(stderr, "error: TMSBITS must contain 1 to 64 binary digits\n");
            return 2;
        }
    }

    printf("clock=0 state=%s\n", state_names[state]);
    for (index = 0U; index < length; ++index) {
        unsigned int tms = bits[index] == '1' ? 1U : 0U;
        state = transitions[state][tms];
        printf("clock=%zu tms=%u state=%s\n", index + 1U, tms,
               state_names[state]);
    }
    printf("final=%s clocks=%zu\n", state_names[state], length);
    return 0;
}

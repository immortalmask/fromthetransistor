#ifndef FTT_TEST_SUPPORT_H
#define FTT_TEST_SUPPORT_H

#ifndef _POSIX_C_SOURCE
#define _POSIX_C_SOURCE 200809L
#endif

#include <errno.h>
#include <signal.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define CTEST_ARRAY_LEN(values) (sizeof(values) / sizeof((values)[0]))
#define CTEST_MAX_ARGUMENTS 32U
#define CTEST_MAX_OUTPUT_BYTES (128U * 1024U)
#define CTEST_TIMEOUT_SECONDS 5U

enum ctest_output_mode {
    CTEST_EXACT = 0,
    CTEST_CONTAINS = 1,
};

struct ctest_case {
    const char *name;
    const char *const *arguments;
    const unsigned char *input;
    size_t input_length;
    int expected_exit;
    const char *expected_output;
    enum ctest_output_mode output_mode;
};

#define CTEST_CASE(test_name, test_arguments, test_input, test_exit, test_output, test_mode) \
    {                                                                                       \
        .name = (test_name),                                                                \
        .arguments = (test_arguments),                                                      \
        .input = (const unsigned char *)(test_input),                                       \
        .input_length = sizeof(test_input) - 1U,                                            \
        .expected_exit = (test_exit),                                                       \
        .expected_output = (test_output),                                                   \
        .output_mode = (test_mode),                                                         \
    }

static volatile sig_atomic_t ctest_child_pid = -1;
static volatile sig_atomic_t ctest_timed_out = 0;

static void ctest_timeout_handler(int signal_number) {
    (void)signal_number;
    ctest_timed_out = 1;
    if (ctest_child_pid > 0) {
        (void)kill((pid_t)ctest_child_pid, SIGKILL);
    }
}

static int ctest_close(int descriptor) {
    int result;
    do {
        result = close(descriptor);
    } while (result < 0 && errno == EINTR);
    return result;
}

static bool ctest_write_all(
    int descriptor,
    const unsigned char *data,
    size_t length
) {
    size_t written = 0U;
    while (written < length) {
        const ssize_t result = write(descriptor, data + written, length - written);
        if (result > 0) {
            written += (size_t)result;
            continue;
        }
        if (result < 0 && errno == EINTR) {
            continue;
        }
        if (result < 0 && errno == EPIPE) {
            return true;
        }
        return false;
    }
    return true;
}

static size_t ctest_argument_count(const char *const *arguments) {
    size_t count = 0U;
    while (arguments[count] != NULL && count <= CTEST_MAX_ARGUMENTS) {
        count += 1U;
    }
    return count;
}

static bool ctest_output_matches(
    const unsigned char *actual,
    size_t actual_length,
    const char *expected,
    enum ctest_output_mode mode
) {
    const size_t expected_length = strlen(expected);
    if (memchr(actual, '\0', actual_length) != NULL) {
        return false;
    }
    if (mode == CTEST_EXACT) {
        return actual_length == expected_length
            && memcmp(actual, expected, expected_length) == 0;
    }
    if (mode == CTEST_CONTAINS) {
        if (expected_length == 0U || expected_length > actual_length) {
            return false;
        }
        for (size_t offset = 0U; offset <= actual_length - expected_length; offset += 1U) {
            if (memcmp(actual + offset, expected, expected_length) == 0) {
                return true;
            }
        }
    }
    return false;
}

static int ctest_run_one(
    const char *program,
    const struct ctest_case *test,
    size_t ordinal
) {
    int input_pipe[2];
    int output_pipe[2];
    if (pipe(input_pipe) != 0) {
        perror("pipe");
        return 1;
    }
    if (pipe(output_pipe) != 0) {
        perror("pipe");
        (void)ctest_close(input_pipe[0]);
        (void)ctest_close(input_pipe[1]);
        return 1;
    }

    const size_t argument_count = ctest_argument_count(test->arguments);
    if (argument_count > CTEST_MAX_ARGUMENTS) {
        fprintf(stderr, "not ok %zu - %s (too many arguments)\n", ordinal, test->name);
        (void)ctest_close(input_pipe[0]);
        (void)ctest_close(input_pipe[1]);
        (void)ctest_close(output_pipe[0]);
        (void)ctest_close(output_pipe[1]);
        return 1;
    }

    const pid_t child = fork();
    if (child < 0) {
        perror("fork");
        (void)ctest_close(input_pipe[0]);
        (void)ctest_close(input_pipe[1]);
        (void)ctest_close(output_pipe[0]);
        (void)ctest_close(output_pipe[1]);
        return 1;
    }
    if (child == 0) {
        char *child_argv[CTEST_MAX_ARGUMENTS + 2U];
        child_argv[0] = (char *)program;
        for (size_t index = 0U; index < argument_count; index += 1U) {
            child_argv[index + 1U] = (char *)test->arguments[index];
        }
        child_argv[argument_count + 1U] = NULL;

        if (
            dup2(input_pipe[0], STDIN_FILENO) < 0
            || dup2(output_pipe[1], STDOUT_FILENO) < 0
            || dup2(output_pipe[1], STDERR_FILENO) < 0
        ) {
            _exit(126);
        }
        (void)ctest_close(input_pipe[0]);
        (void)ctest_close(input_pipe[1]);
        (void)ctest_close(output_pipe[0]);
        (void)ctest_close(output_pipe[1]);
        execv(program, child_argv);
        _exit(127);
    }

    (void)ctest_close(input_pipe[0]);
    (void)ctest_close(output_pipe[1]);
    ctest_child_pid = (sig_atomic_t)child;
    ctest_timed_out = 0;
    (void)alarm(CTEST_TIMEOUT_SECONDS);

    const bool input_ok = ctest_write_all(
        input_pipe[1], test->input, test->input_length
    );
    (void)ctest_close(input_pipe[1]);

    unsigned char output[CTEST_MAX_OUTPUT_BYTES + 1U];
    unsigned char chunk[4096];
    size_t output_length = 0U;
    bool output_truncated = false;
    for (;;) {
        const ssize_t result = read(output_pipe[0], chunk, sizeof(chunk));
        if (result == 0) {
            break;
        }
        if (result < 0) {
            if (errno == EINTR) {
                continue;
            }
            break;
        }
        const size_t bytes_read = (size_t)result;
        const size_t remaining = CTEST_MAX_OUTPUT_BYTES - output_length;
        const size_t to_copy = bytes_read < remaining ? bytes_read : remaining;
        if (to_copy > 0U) {
            memcpy(output + output_length, chunk, to_copy);
            output_length += to_copy;
        }
        if (bytes_read > to_copy) {
            output_truncated = true;
        }
    }
    (void)ctest_close(output_pipe[0]);

    int status = 0;
    pid_t waited;
    do {
        waited = waitpid(child, &status, 0);
    } while (waited < 0 && errno == EINTR);
    (void)alarm(0U);
    ctest_child_pid = -1;

    int actual_exit = 255;
    if (waited == child && WIFEXITED(status)) {
        actual_exit = WEXITSTATUS(status);
    } else if (waited == child && WIFSIGNALED(status)) {
        actual_exit = 128 + WTERMSIG(status);
    }
    const bool output_ok = !output_truncated && ctest_output_matches(
        output, output_length, test->expected_output, test->output_mode
    );
    const bool passed = input_ok
        && ctest_timed_out == 0
        && actual_exit == test->expected_exit
        && output_ok;
    if (passed) {
        printf("ok %zu - %s\n", ordinal, test->name);
        return 0;
    }

    fprintf(
        stderr,
        "not ok %zu - %s\n"
        "  exit: expected %d, got %d%s\n"
        "  output (%s): expected %s\n"
        "  actual: ",
        ordinal,
        test->name,
        test->expected_exit,
        actual_exit,
        ctest_timed_out != 0 ? " (timeout)" : "",
        test->output_mode == CTEST_EXACT ? "exact" : "contains",
        test->expected_output
    );
    if (output_length > 0U) {
        (void)fwrite(output, 1U, output_length, stderr);
    }
    if (output_length == 0U || output[output_length - 1U] != (unsigned char)'\n') {
        fputc('\n', stderr);
    }
    if (output_truncated) {
        fputs("  [output truncated]\n", stderr);
    }
    return 1;
}

static int ctest_main(
    int argc,
    char **argv,
    const struct ctest_case *cases,
    size_t case_count
) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s PROGRAM\n", argv[0]);
        return 2;
    }
    if (case_count == 0U) {
        fputs("test suite must contain at least one case\n", stderr);
        return 2;
    }
    if (access(argv[1], X_OK) != 0) {
        perror(argv[1]);
        return 2;
    }

    struct sigaction action;
    struct sigaction previous;
    struct sigaction pipe_action;
    struct sigaction previous_pipe;
    memset(&action, 0, sizeof(action));
    action.sa_handler = ctest_timeout_handler;
    if (sigemptyset(&action.sa_mask) != 0 || sigaction(SIGALRM, &action, &previous) != 0) {
        perror("sigaction");
        return 2;
    }
    memset(&pipe_action, 0, sizeof(pipe_action));
    pipe_action.sa_handler = SIG_IGN;
    if (
        sigemptyset(&pipe_action.sa_mask) != 0
        || sigaction(SIGPIPE, &pipe_action, &previous_pipe) != 0
    ) {
        perror("sigaction SIGPIPE");
        (void)sigaction(SIGALRM, &previous, NULL);
        return 2;
    }

    printf("1..%zu\n", case_count);
    size_t failed = 0U;
    for (size_t index = 0U; index < case_count; index += 1U) {
        if (ctest_run_one(argv[1], &cases[index], index + 1U) != 0) {
            failed += 1U;
        }
    }
    if (
        sigaction(SIGPIPE, &previous_pipe, NULL) != 0
        || sigaction(SIGALRM, &previous, NULL) != 0
    ) {
        perror("sigaction restore");
        return 2;
    }
    printf(
        "# %zu/%zu native C cases passed\n",
        case_count - failed,
        case_count
    );
    return failed == 0U ? 0 : 1;
}

#endif

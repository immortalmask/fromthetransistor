CC ?= cc
SOURCE ?= solution/main.c
BUILD_DIR ?= .c-test-build
TEST_SUPPORT_DIR ?= ..

STRICT_CFLAGS = -std=c17 -O2 -Wall -Wextra -Werror -Wpedantic \
	-Wconversion -Wsign-conversion -Wshadow
PROGRAM = $(BUILD_DIR)/program
TEST_RUNNER = $(BUILD_DIR)/test-runner

.PHONY: test clean

test:
	@mkdir -p "$(BUILD_DIR)"
	$(CC) $(STRICT_CFLAGS) "$(SOURCE)" -o "$(PROGRAM)"
	$(CC) $(STRICT_CFLAGS) -I"$(TEST_SUPPORT_DIR)" tests/test.c -o "$(TEST_RUNNER)"
	@"$(TEST_RUNNER)" "$(PROGRAM)"

clean:
	@rm -rf -- "$(BUILD_DIR)"

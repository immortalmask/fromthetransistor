#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum {
    REGISTER_COUNT = 16,
    MEMORY_SIZE = 256,
    MAX_PROGRAM_WORDS = 128,
    EXECUTION_BUDGET = 256
};

static int hex_value(char character)
{
    if (character >= '0' && character <= '9') {
        return character - '0';
    }
    if (character >= 'a' && character <= 'f') {
        return character - 'a' + 10;
    }
    if (character >= 'A' && character <= 'F') {
        return character - 'A' + 10;
    }
    return -1;
}

static bool parse_word(const char *text, uint16_t *result)
{
    unsigned int value = 0U;
    size_t index;

    if (strlen(text) != 4U) {
        return false;
    }
    for (index = 0U; index < 4U; ++index) {
        int digit = hex_value(text[index]);
        if (digit < 0) {
            return false;
        }
        value = value * 16U + (unsigned int)digit;
    }
    *result = (uint16_t)value;
    return true;
}

static void print_state(size_t steps, size_t pc,
                        const uint8_t registers[REGISTER_COUNT],
                        const uint8_t memory[MEMORY_SIZE])
{
    size_t index;
    bool any_memory = false;

    printf("halted steps=%zu pc=%zu\n", steps, pc);
    fputs("registers", stdout);
    for (index = 0U; index < REGISTER_COUNT; ++index) {
        printf(" r%zu=%02x", index, (unsigned int)registers[index]);
    }
    putchar('\n');
    fputs("memory", stdout);
    for (index = 0U; index < MEMORY_SIZE; ++index) {
        if (memory[index] != 0U) {
            printf(" %02zx=%02x", index, (unsigned int)memory[index]);
            any_memory = true;
        }
    }
    if (!any_memory) {
        fputs(" empty", stdout);
    }
    putchar('\n');
}

static int execute(const uint16_t *program, size_t word_count)
{
    uint8_t registers[REGISTER_COUNT] = {0};
    uint8_t memory[MEMORY_SIZE] = {0};
    size_t pc = 0U;
    size_t steps;

    for (steps = 0U; steps < EXECUTION_BUDGET; ++steps) {
        uint16_t word;
        unsigned int opcode;
        unsigned int first;
        unsigned int second;
        unsigned int low_byte;

        if (pc >= word_count) {
            fprintf(stderr, "error: pc %zu is outside program (%zu words)\n", pc,
                    word_count);
            return 3;
        }
        word = program[pc];
        opcode = (unsigned int)(word >> 12U);
        first = (unsigned int)((word >> 8U) & UINT16_C(0x000f));
        second = (unsigned int)((word >> 4U) & UINT16_C(0x000f));
        low_byte = (unsigned int)(word & UINT16_C(0x00ff));

        switch (opcode) {
        case 0U:
            if (word != 0U) {
                goto invalid_encoding;
            }
            print_state(steps + 1U, pc, registers, memory);
            return 0;
        case 1U:
            registers[first] = (uint8_t)low_byte;
            ++pc;
            break;
        case 2U:
            if ((word & UINT16_C(0x000f)) != 0U) {
                goto invalid_encoding;
            }
            registers[first] = (uint8_t)(registers[first] + registers[second]);
            ++pc;
            break;
        case 3U:
            if ((word & UINT16_C(0x000f)) != 0U) {
                goto invalid_encoding;
            }
            registers[first] = (uint8_t)(registers[first] ^ registers[second]);
            ++pc;
            break;
        case 4U:
            registers[first] = memory[low_byte];
            ++pc;
            break;
        case 5U:
            memory[low_byte] = registers[first];
            ++pc;
            break;
        case 6U:
            pc = (size_t)(word & UINT16_C(0x0fff));
            break;
        case 7U:
            if (registers[first] == 0U) {
                int offset = low_byte <= 127U ? (int)low_byte : (int)low_byte - 256;
                long target = (long)pc + 1L + (long)offset;
                if (target < 0L) {
                    fprintf(stderr, "error: branch target %ld is outside program\n",
                            target);
                    return 3;
                }
                pc = (size_t)target;
            } else {
                ++pc;
            }
            break;
        default:
            goto invalid_encoding;
        }
        continue;

invalid_encoding:
        fprintf(stderr, "error: invalid instruction 0x%04x at pc %zu\n",
                (unsigned int)word, pc);
        return 3;
    }
    fprintf(stderr, "error: execution budget exceeded after 256 steps\n");
    return 3;
}

int main(int argc, char **argv)
{
    uint16_t program[MAX_PROGRAM_WORDS];
    int index;

    if (argc < 2 || argc > MAX_PROGRAM_WORDS + 1) {
        fprintf(stderr, "error: expected 1 to 128 instruction words\n");
        return 2;
    }
    for (index = 1; index < argc; ++index) {
        if (!parse_word(argv[index], &program[index - 1])) {
            fprintf(stderr, "error: word %d is not exactly four hexadecimal digits\n",
                    index - 1);
            return 2;
        }
    }
    return execute(program, (size_t)(argc - 1));
}

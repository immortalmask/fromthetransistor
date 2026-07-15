#include <ctype.h>
#include <errno.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { MAX_INSTRUCTIONS = 128 };

typedef enum {
    OP_PUSH,
    OP_ADD,
    OP_SUB,
    OP_MUL
} Opcode;

typedef struct {
    Opcode opcode;
    int64_t operand;
} Instruction;

typedef struct {
    const char *cursor;
    Instruction code[MAX_INSTRUCTIONS];
    size_t count;
    const char *error;
} Parser;

static void skip_space(Parser *parser)
{
    while (isspace((unsigned char)*parser->cursor) != 0) {
        ++parser->cursor;
    }
}

static bool emit(Parser *parser, Opcode opcode, int64_t operand)
{
    if (parser->count == MAX_INSTRUCTIONS) {
        parser->error = "expression is too complex";
        return false;
    }
    parser->code[parser->count].opcode = opcode;
    parser->code[parser->count].operand = operand;
    ++parser->count;
    return true;
}

static bool parse_expression(Parser *parser, int64_t *value);

static bool checked_add(int64_t left, int64_t right, int64_t *result)
{
    if ((right > 0 && left > INT64_MAX - right)
        || (right < 0 && left < INT64_MIN - right)) {
        return false;
    }
    *result = left + right;
    return true;
}

static bool checked_subtract(int64_t left, int64_t right, int64_t *result)
{
    if ((right > 0 && left < INT64_MIN + right)
        || (right < 0 && left > INT64_MAX + right)) {
        return false;
    }
    *result = left - right;
    return true;
}

static bool checked_multiply(int64_t left, int64_t right, int64_t *result)
{
    if (left == 0 || right == 0) {
        *result = 0;
        return true;
    }
    if ((left == -1 && right == INT64_MIN)
        || (right == -1 && left == INT64_MIN)) {
        return false;
    }
    if (left > 0) {
        if ((right > 0 && left > INT64_MAX / right)
            || (right < 0 && right < INT64_MIN / left)) {
            return false;
        }
    } else if ((right > 0 && left < INT64_MIN / right)
               || (right < 0 && left < INT64_MAX / right)) {
        return false;
    }
    *result = left * right;
    return true;
}

static bool parse_factor(Parser *parser, int64_t *value)
{
    char *end = NULL;
    long long parsed;

    skip_space(parser);
    if (*parser->cursor == '(') {
        ++parser->cursor;
        if (!parse_expression(parser, value)) {
            return false;
        }
        skip_space(parser);
        if (*parser->cursor != ')') {
            parser->error = "expected ')'";
            return false;
        }
        ++parser->cursor;
        return true;
    }
    if (isdigit((unsigned char)*parser->cursor) == 0) {
        parser->error = "expected integer or '('";
        return false;
    }
    errno = 0;
    parsed = strtoll(parser->cursor, &end, 10);
    if (errno == ERANGE || end == parser->cursor) {
        parser->error = "integer is out of range";
        return false;
    }
    parser->cursor = end;
    *value = (int64_t)parsed;
    return emit(parser, OP_PUSH, *value);
}

static bool parse_term(Parser *parser, int64_t *value)
{
    int64_t right;

    if (!parse_factor(parser, value)) {
        return false;
    }
    for (;;) {
        skip_space(parser);
        if (*parser->cursor != '*') {
            return true;
        }
        ++parser->cursor;
        if (!parse_factor(parser, &right)) {
            return false;
        }
        if (!checked_multiply(*value, right, value)) {
            parser->error = "arithmetic overflow";
            return false;
        }
        if (!emit(parser, OP_MUL, 0)) {
            return false;
        }
    }
}

static bool parse_expression(Parser *parser, int64_t *value)
{
    int64_t right;
    char operator_character;

    if (!parse_term(parser, value)) {
        return false;
    }
    for (;;) {
        skip_space(parser);
        operator_character = *parser->cursor;
        if (operator_character != '+' && operator_character != '-') {
            return true;
        }
        ++parser->cursor;
        if (!parse_term(parser, &right)) {
            return false;
        }
        if (operator_character == '+') {
            if (!checked_add(*value, right, value)) {
                parser->error = "arithmetic overflow";
                return false;
            }
            if (!emit(parser, OP_ADD, 0)) {
                return false;
            }
        } else {
            if (!checked_subtract(*value, right, value)) {
                parser->error = "arithmetic overflow";
                return false;
            }
            if (!emit(parser, OP_SUB, 0)) {
                return false;
            }
        }
    }
}

static void print_program(const Parser *parser, int64_t result)
{
    size_t index;

    for (index = 0; index < parser->count; ++index) {
        switch (parser->code[index].opcode) {
        case OP_PUSH:
            printf("PUSH %" PRId64 "\n", parser->code[index].operand);
            break;
        case OP_ADD:
            puts("ADD");
            break;
        case OP_SUB:
            puts("SUB");
            break;
        case OP_MUL:
            puts("MUL");
            break;
        }
    }
    printf("RESULT %" PRId64 "\n", result);
}

int main(int argc, char **argv)
{
    Parser parser = {0};
    int64_t result;

    if (argc != 2) {
        fputs("error: expected one expression\n", stderr);
        return 2;
    }
    parser.cursor = argv[1];
    if (!parse_expression(&parser, &result)) {
        fprintf(stderr, "error: %s\n", parser.error);
        return 2;
    }
    skip_space(&parser);
    if (*parser.cursor != '\0') {
        fputs("error: unexpected trailing input\n", stderr);
        return 2;
    }
    print_program(&parser, result);
    return 0;
}

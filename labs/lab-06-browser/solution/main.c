#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

enum {
    MAX_RESPONSE = 8192,
    MAX_REASON = 63,
    MAX_TITLE = 255,
    MAX_RENDERED = 4096
};

struct http_view {
    unsigned int status;
    char reason[MAX_REASON + 1];
    const char *body;
    size_t body_length;
};

struct html_result {
    char title[MAX_TITLE + 1];
    size_t title_length;
    char body[MAX_RENDERED + 1];
    size_t body_length;
};

static char ascii_lower(char character)
{
    if (character >= 'A' && character <= 'Z') {
        return (char)(character - 'A' + 'a');
    }
    return character;
}

static bool span_equal_case(const char *text, size_t length, const char *literal)
{
    size_t index;

    if (strlen(literal) != length) {
        return false;
    }
    for (index = 0U; index < length; ++index) {
        if (ascii_lower(text[index]) != ascii_lower(literal[index])) {
            return false;
        }
    }
    return true;
}

static bool ascii_space(char character)
{
    return character == ' ' || character == '\t' || character == '\r' ||
           character == '\n' || character == '\f' || character == '\v';
}

static bool parse_decimal(const char *text, size_t length, size_t *value)
{
    size_t result = 0U;
    size_t index;

    if (length == 0U) {
        return false;
    }
    for (index = 0U; index < length; ++index) {
        unsigned int digit;
        if (text[index] < '0' || text[index] > '9') {
            return false;
        }
        digit = (unsigned int)(text[index] - '0');
        if (result > (size_t)MAX_RESPONSE / 10U) {
            return false;
        }
        result = result * 10U + (size_t)digit;
        if (result > (size_t)MAX_RESPONSE) {
            return false;
        }
    }
    *value = result;
    return true;
}

static bool valid_header_name(const char *text, size_t length)
{
    size_t index;

    if (length == 0U) {
        return false;
    }
    for (index = 0U; index < length; ++index) {
        char character = text[index];
        bool alphanumeric = (character >= 'a' && character <= 'z') ||
                            (character >= 'A' && character <= 'Z') ||
                            (character >= '0' && character <= '9');
        if (!alphanumeric && character != '-') {
            return false;
        }
    }
    return true;
}

static bool valid_header_value(const char *text, size_t length)
{
    size_t index;

    for (index = 0U; index < length; ++index) {
        unsigned char character = (unsigned char)text[index];
        if (character != (unsigned char)'\t' &&
            (character < 0x20U || character > 0x7eU)) {
            return false;
        }
    }
    return true;
}

static bool parse_status_line(const char *line, size_t length,
                              struct http_view *view)
{
    size_t reason_length;
    size_t index;

    if (length < 14U ||
        (memcmp(line, "HTTP/1.0 ", 9U) != 0 &&
         memcmp(line, "HTTP/1.1 ", 9U) != 0) ||
        line[9] < '0' || line[9] > '9' || line[10] < '0' || line[10] > '9' ||
        line[11] < '0' || line[11] > '9' || line[12] != ' ') {
        fprintf(stderr, "error: malformed HTTP status line\n");
        return false;
    }
    reason_length = length - 13U;
    if (reason_length == 0U || reason_length > MAX_REASON) {
        fprintf(stderr, "error: malformed HTTP status line\n");
        return false;
    }
    for (index = 0U; index < reason_length; ++index) {
        unsigned char character = (unsigned char)line[index + 13U];
        if (character < 0x20U || character > 0x7eU) {
            fprintf(stderr, "error: malformed HTTP status line\n");
            return false;
        }
        view->reason[index] = (char)character;
    }
    view->reason[reason_length] = '\0';
    view->status = (unsigned int)(line[9] - '0') * 100U +
                   (unsigned int)(line[10] - '0') * 10U +
                   (unsigned int)(line[11] - '0');
    return true;
}

static bool parse_http(char *response, size_t response_length,
                       struct http_view *view)
{
    char *header_end = strstr(response, "\r\n\r\n");
    char *status_end;
    char *cursor;
    bool saw_content_length = false;
    size_t content_length = 0U;

    if (header_end == NULL) {
        fprintf(stderr,
                "error: malformed HTTP framing (missing CRLF header terminator)\n");
        return false;
    }
    status_end = strstr(response, "\r\n");
    if (status_end == NULL || status_end > header_end ||
        !parse_status_line(response, (size_t)(status_end - response), view)) {
        if (status_end == NULL || status_end > header_end) {
            fprintf(stderr, "error: malformed HTTP status line\n");
        }
        return false;
    }

    cursor = status_end + 2;
    while (cursor < header_end) {
        char *line_end = strstr(cursor, "\r\n");
        char *colon;
        size_t line_length;
        size_t name_length;
        const char *value;
        size_t value_length;

        if (line_end == NULL || line_end > header_end) {
            fprintf(stderr, "error: malformed HTTP header line\n");
            return false;
        }
        line_length = (size_t)(line_end - cursor);
        colon = memchr(cursor, ':', line_length);
        if (colon == NULL) {
            fprintf(stderr, "error: malformed HTTP header line\n");
            return false;
        }
        name_length = (size_t)(colon - cursor);
        if (!valid_header_name(cursor, name_length)) {
            fprintf(stderr, "error: malformed HTTP header line\n");
            return false;
        }
        value = colon + 1;
        value_length = (size_t)(line_end - value);
        while (value_length > 0U && (*value == ' ' || *value == '\t')) {
            ++value;
            --value_length;
        }
        while (value_length > 0U &&
               (value[value_length - 1U] == ' ' || value[value_length - 1U] == '\t')) {
            --value_length;
        }
        if (!valid_header_value(value, value_length)) {
            fprintf(stderr, "error: malformed HTTP header line\n");
            return false;
        }
        if (span_equal_case(cursor, name_length, "Content-Length")) {
            if (saw_content_length ||
                !parse_decimal(value, value_length, &content_length)) {
                fprintf(stderr, "error: invalid or duplicate Content-Length header\n");
                return false;
            }
            saw_content_length = true;
        }
        cursor = line_end + 2;
    }
    if (!saw_content_length) {
        fprintf(stderr, "error: missing Content-Length header\n");
        return false;
    }

    view->body = header_end + 4;
    view->body_length = response_length - (size_t)(view->body - response);
    if (content_length != view->body_length) {
        fprintf(stderr, "error: Content-Length %zu does not match %zu body bytes\n",
                content_length, view->body_length);
        return false;
    }
    return true;
}

static bool append_character(char *output, size_t capacity, size_t *length,
                             char character)
{
    if (*length >= capacity) {
        fprintf(stderr, "error: rendered HTML exceeds output limit\n");
        return false;
    }
    output[*length] = character;
    ++*length;
    return true;
}

static bool append_text_character(char *output, size_t capacity, size_t *length,
                                  char character)
{
    if (ascii_space(character)) {
        if (*length == 0U || output[*length - 1U] == ' ' ||
            output[*length - 1U] == '\n') {
            return true;
        }
        character = ' ';
    }
    return append_character(output, capacity, length, character);
}

static bool append_break(char *output, size_t capacity, size_t *length)
{
    if (*length > 0U && output[*length - 1U] == ' ') {
        --*length;
    }
    if (*length == 0U || output[*length - 1U] == '\n') {
        return true;
    }
    return append_character(output, capacity, length, '\n');
}

static bool decode_entity(const char *text, size_t remaining, char *character,
                          size_t *consumed)
{
    static const struct {
        const char *spelling;
        char value;
    } entities[] = {
        {"&amp;", '&'}, {"&lt;", '<'}, {"&gt;", '>'},
        {"&quot;", '"'}, {"&nbsp;", ' '}
    };
    size_t index;

    for (index = 0U; index < sizeof(entities) / sizeof(entities[0]); ++index) {
        size_t length = strlen(entities[index].spelling);
        if (length <= remaining &&
            memcmp(text, entities[index].spelling, length) == 0) {
            *character = entities[index].value;
            *consumed = length;
            return true;
        }
    }
    return false;
}

static bool append_segment(const char *text, size_t length, char *output,
                           size_t capacity, size_t *output_length)
{
    size_t index = 0U;

    while (index < length) {
        char character = text[index];
        size_t consumed = 1U;
        if (character == '&') {
            if (!decode_entity(text + index, length - index, &character, &consumed)) {
                fprintf(stderr, "error: unsupported or malformed HTML entity\n");
                return false;
            }
        }
        if ((unsigned char)character < 0x20U && !ascii_space(character)) {
            fprintf(stderr, "error: unsupported control byte in HTML text\n");
            return false;
        }
        if (!append_text_character(output, capacity, output_length, character)) {
            return false;
        }
        index += consumed;
    }
    return true;
}

static void trim_output(char *output, size_t *length)
{
    while (*length > 0U &&
           (output[*length - 1U] == ' ' || output[*length - 1U] == '\n')) {
        --*length;
    }
    output[*length] = '\0';
}

static bool whitespace_only(const char *text, size_t length)
{
    size_t index;
    for (index = 0U; index < length; ++index) {
        if (!ascii_space(text[index])) {
            return false;
        }
    }
    return true;
}

static bool diagnostic_tag(const char *tag, size_t length)
{
    size_t index;

    if (length == 0U || length > 32U) {
        return false;
    }
    for (index = 0U; index < length; ++index) {
        char character = tag[index];
        bool alphanumeric = (character >= 'a' && character <= 'z') ||
                            (character >= 'A' && character <= 'Z') ||
                            (character >= '0' && character <= '9');
        if (!alphanumeric && character != '/') {
            return false;
        }
    }
    return true;
}

static bool parse_html(const char *html, size_t length, struct html_result *result)
{
    size_t position = 0U;
    bool in_title = false;
    bool in_body = false;
    bool saw_title = false;
    bool saw_body = false;
    bool closed_body = false;

    result->title_length = 0U;
    result->body_length = 0U;

    while (position < length) {
        const char *open = memchr(html + position, '<', length - position);
        size_t text_end = open == NULL ? length : (size_t)(open - html);
        size_t text_length = text_end - position;

        if (text_length > 0U) {
            if (in_title) {
                if (!append_segment(html + position, text_length, result->title,
                                    MAX_TITLE, &result->title_length)) {
                    return false;
                }
            } else if (in_body) {
                if (!append_segment(html + position, text_length, result->body,
                                    MAX_RENDERED, &result->body_length)) {
                    return false;
                }
            } else if (!whitespace_only(html + position, text_length)) {
                fprintf(stderr, "error: HTML text appears outside title or body\n");
                return false;
            }
        }
        if (open == NULL) {
            position = length;
            break;
        }

        {
            const char *close = memchr(open + 1, '>',
                                      length - (size_t)(open + 1 - html));
            const char *tag;
            size_t tag_length;

            if (close == NULL) {
                fprintf(stderr, "error: unterminated HTML tag\n");
                return false;
            }
            tag = open + 1;
            tag_length = (size_t)(close - tag);
            if (span_equal_case(tag, tag_length, "title")) {
                if (in_title || in_body || saw_title || saw_body) {
                    fprintf(stderr, "error: invalid HTML title structure\n");
                    return false;
                }
                in_title = true;
                saw_title = true;
            } else if (span_equal_case(tag, tag_length, "/title")) {
                if (!in_title) {
                    fprintf(stderr, "error: invalid HTML title structure\n");
                    return false;
                }
                in_title = false;
            } else if (span_equal_case(tag, tag_length, "body")) {
                if (in_title || in_body || saw_body) {
                    fprintf(stderr, "error: invalid HTML body structure\n");
                    return false;
                }
                in_body = true;
                saw_body = true;
            } else if (span_equal_case(tag, tag_length, "/body")) {
                if (!in_body) {
                    fprintf(stderr, "error: invalid HTML body structure\n");
                    return false;
                }
                in_body = false;
                closed_body = true;
            } else if (span_equal_case(tag, tag_length, "p") ||
                       span_equal_case(tag, tag_length, "/p") ||
                       span_equal_case(tag, tag_length, "h1") ||
                       span_equal_case(tag, tag_length, "/h1") ||
                       span_equal_case(tag, tag_length, "br") ||
                       span_equal_case(tag, tag_length, "br/")) {
                if (!in_body ||
                    !append_break(result->body, MAX_RENDERED,
                                  &result->body_length)) {
                    if (!in_body) {
                        fprintf(stderr, "error: body tag appears outside body\n");
                    }
                    return false;
                }
            } else if (span_equal_case(tag, tag_length, "strong") ||
                       span_equal_case(tag, tag_length, "/strong") ||
                       span_equal_case(tag, tag_length, "em") ||
                       span_equal_case(tag, tag_length, "/em")) {
                if (!in_body) {
                    fprintf(stderr, "error: inline tag appears outside body\n");
                    return false;
                }
            } else if (!span_equal_case(tag, tag_length, "html") &&
                       !span_equal_case(tag, tag_length, "/html") &&
                       !span_equal_case(tag, tag_length, "head") &&
                       !span_equal_case(tag, tag_length, "/head")) {
                if (!diagnostic_tag(tag, tag_length)) {
                    fprintf(stderr, "error: malformed HTML tag\n");
                } else {
                    fprintf(stderr, "error: unsupported HTML tag <%.*s>\n",
                            (int)tag_length, tag);
                }
                return false;
            }
            position = (size_t)(close - html) + 1U;
        }
    }

    if (in_title || in_body || !saw_body || !closed_body) {
        fprintf(stderr, "error: unclosed or missing HTML title/body structure\n");
        return false;
    }
    trim_output(result->title, &result->title_length);
    trim_output(result->body, &result->body_length);
    return true;
}

int main(int argc, char **argv)
{
    char response[MAX_RESPONSE + 2];
    size_t response_length;
    struct http_view view;
    struct html_result result;

    (void)argv;
    if (argc != 1) {
        fprintf(stderr, "error: this program reads one HTTP response from stdin\n");
        return 2;
    }
    response_length = fread(response, 1U, MAX_RESPONSE + 1U, stdin);
    if (ferror(stdin)) {
        fprintf(stderr, "error: failed to read HTTP response\n");
        return 2;
    }
    if (response_length > MAX_RESPONSE) {
        fprintf(stderr, "error: HTTP response exceeds 8192-byte limit\n");
        return 2;
    }
    if (memchr(response, '\0', response_length) != NULL) {
        fprintf(stderr, "error: HTTP response contains a NUL byte\n");
        return 2;
    }
    response[response_length] = '\0';

    if (!parse_http(response, response_length, &view) ||
        !parse_html(view.body, view.body_length, &result)) {
        return 2;
    }
    printf("status=%u %s\n", view.status, view.reason);
    printf("title=%s\n", result.title_length == 0U ? "(none)" : result.title);
    puts("body:");
    if (result.body_length > 0U) {
        fwrite(result.body, 1U, result.body_length, stdout);
        putchar('\n');
    }
    return 0;
}

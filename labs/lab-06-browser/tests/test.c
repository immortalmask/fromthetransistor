/* Generated from lab.json by tools/sync_native_c_tests.py. */
#include "test_support.h"

static const char *const ARGS_01[] = {NULL};
static const char *const ARGS_02[] = {NULL};
static const char *const ARGS_03[] = {NULL};
static const char *const ARGS_04[] = {NULL};
static const char *const ARGS_05[] = {NULL};
static const char *const ARGS_06[] = {NULL};
static const char *const ARGS_07[] = {NULL};
static const char *const ARGS_08[] = {NULL};
static const char *const ARGS_09[] = {NULL};
static const char *const ARGS_10[] = {NULL};
static const char *const ARGS_11[] = {NULL};
static const char *const ARGS_12[] = {NULL};

static const struct ctest_case CASES[] = {
    CTEST_CASE(
        "render-title-headline-and-paragraph",
        ARGS_01,
        "HTTP/1.1 200 OK\r\nContent-Length: 96\r\nContent-Type: text/html\r\n\r\n<html><head><title>Demo</title></head><body><h1>Hello</h1><p>Bytes &amp; bits.</p></body></html>",
        0,
        "status=200 OK\ntitle=Demo\nbody:\nHello\nBytes & bits.\n",
        CTEST_EXACT),
    CTEST_CASE(
        "preserve-non-success-status",
        ARGS_02,
        "HTTP/1.0 404 Not Found\r\nContent-Length: 60\r\n\r\n<html><body><p>Not <strong>found</strong>.</p></body></html>",
        0,
        "status=404 Not Found\ntitle=(none)\nbody:\nNot found.\n",
        CTEST_EXACT),
    CTEST_CASE(
        "normalize-whitespace-breaks-and-entities",
        ARGS_03,
        "HTTP/1.1 200 OK\r\ncontent-length: 107\r\n\r\n<html><head><title>  Tiny   Web </title></head><body>one<br>two &lt; three<br/>four&nbsp;five</body></html>",
        0,
        "status=200 OK\ntitle=Tiny Web\nbody:\none\ntwo < three\nfour five\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-lf-only-framing",
        ARGS_04,
        "HTTP/1.1 200 OK\nContent-Length: 0\n\n",
        2,
        "error: malformed HTTP framing (missing CRLF header terminator)\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-content-length-mismatch",
        ARGS_05,
        "HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\ntest",
        2,
        "error: Content-Length 5 does not match 4 body bytes\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-unsupported-tag",
        ARGS_06,
        "HTTP/1.1 200 OK\r\nContent-Length: 44\r\n\r\n<html><body><script>x</script></body></html>",
        2,
        "error: unsupported HTML tag <script>\n",
        CTEST_EXACT),
    CTEST_CASE(
        "http-10-case-insensitive-header-and-tags",
        ARGS_07,
        "HTTP/1.0 204 No Content\r\ncontent-length: 26\r\nX-Test: ok\r\n\r\n<HTML><BODY></BODY></HTML>",
        0,
        "status=204 No Content\ntitle=(none)\nbody:\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-duplicate-content-length-before-html",
        ARGS_08,
        "HTTP/1.1 200 OK\r\nContent-Length: 13\r\ncontent-length: 13\r\n\r\n<body></body>",
        2,
        "error: invalid or duplicate Content-Length header\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-unsupported-entity-without-partial-render",
        ARGS_09,
        "HTTP/1.1 200 OK\r\nContent-Length: 21\r\n\r\n<body>A&copy;B</body>",
        2,
        "error: unsupported or malformed HTML entity\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-unclosed-body-structure",
        ARGS_10,
        "HTTP/1.1 200 OK\r\nContent-Length: 23\r\n\r\n<html><body>text</html>",
        2,
        "error: unclosed or missing HTML title/body structure\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-unsupported-http-version",
        ARGS_11,
        "HTTP/2.0 200 OK\r\nContent-Length: 13\r\n\r\n<body></body>",
        2,
        "error: malformed HTTP status line\n",
        CTEST_EXACT),
    CTEST_CASE(
        "reject-nul-byte-before-protocol-parsing",
        ARGS_12,
        "HTTP/1.1 200 OK\r\nContent-Length: 16\r\n\r\n<body>A\000B</body>",
        2,
        "error: HTTP response contains a NUL byte\n",
        CTEST_EXACT),
};

int main(int argc, char **argv) {
    return ctest_main(argc, argv, CASES, CTEST_ARRAY_LEN(CASES));
}

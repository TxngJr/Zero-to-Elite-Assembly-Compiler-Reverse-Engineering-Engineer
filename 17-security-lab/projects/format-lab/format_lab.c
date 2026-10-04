#include <stdio.h>

static void print_user_text(const char *text) {
#ifdef INJECT_FORMAT_BUG
    /*
     * Intentional course-only bad pattern. The build target demonstrates
     * compiler diagnostics; no untrusted external target is involved.
     */
    printf(text);
#else
    printf("%s", text);
#endif
}

int main(void) {
    print_user_text("literal percent: 100%% complete\n");
    puts("format-lab: OK");
    return 0;
}

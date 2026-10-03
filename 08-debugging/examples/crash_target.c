#include <stdio.h>
#include <string.h>

static int safe_path(void) {
    puts("safe path");
    return 0;
}
static int crash_path(void) {
    volatile int *p = NULL;
    return *p; /* Intentional course-owned crash target for debugger lab. */
}
int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--crash") == 0) return crash_path();
    return safe_path();
}

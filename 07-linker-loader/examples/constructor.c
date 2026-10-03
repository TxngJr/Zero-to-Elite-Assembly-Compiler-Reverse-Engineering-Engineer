#include <stdio.h>
__attribute__((constructor))
static void before_main(void) { puts("constructor"); }
int main(void) {
    puts("main");
    return 0;
}

#include <stdio.h>
__attribute__((weak)) int course_value(void) { return 1; }
int main(void) {
    printf("%d\n", course_value());
    return 0;
}

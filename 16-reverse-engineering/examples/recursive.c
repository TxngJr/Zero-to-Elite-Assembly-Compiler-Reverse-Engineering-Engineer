#include <stdio.h>

__attribute__((noinline))
static long recurrence(long n) {
    if (n <= 1) return n + 1;
    return recurrence(n - 1) + 2 * recurrence(n - 2);
}

int main(void) {
    printf("%ld\n", recurrence(6));
    return 0;
}

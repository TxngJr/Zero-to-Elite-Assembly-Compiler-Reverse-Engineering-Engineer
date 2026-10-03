#include <assert.h>
#include <stdio.h>
static int bounded_square(int x) {
    assert(x >= 0 && x <= 100);
    return x * x;
}
int main(void) {
    printf("%d\n", bounded_square(7));
    return 0;
}

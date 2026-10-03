#include <stdio.h>

int main(void) {
    int x = 42;
    printf("x=%d sizeof(x)=%zu address=%p\n", x, sizeof x, (void *)&x);
    return 0;
}

#include <stdio.h>
int main(void) {
    int x = 10;
    int *p = &x;
    printf("x=%d &x=%p p=%p &p=%p *p=%d\n", x, (void *)&x, (void *)p, (void *)&p, *p);
    *p = 99;
    printf("after *p=99, x=%d\n", x);
    return 0;
}

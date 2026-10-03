#include <stddef.h>
#include <stdio.h>
int main(void) {
    int a[5] = {10,20,30,40,50};
    int *p = a;
    printf("sizeof a=%zu sizeof p=%zu\n", sizeof a, sizeof p);
    printf("a=%p a+1=%p diff=%td\n", (void *)a, (void *)(a+1), (ptrdiff_t)((unsigned char *)(a+1)-(unsigned char *)a));
    printf("&a=%p &a+1=%p diff=%td\n", (void *)&a, (void *)(&a+1), (ptrdiff_t)((unsigned char *)(&a+1)-(unsigned char *)&a));
    return 0;
}

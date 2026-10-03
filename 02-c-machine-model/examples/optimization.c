#include <stdio.h>
static int compute(int x) {
    int constant_part = 6 * 7;
    int unused = x * 100;
    (void)unused;
    return constant_part + x;
}
int main(void){printf("%d\n",compute(0));return 0;}

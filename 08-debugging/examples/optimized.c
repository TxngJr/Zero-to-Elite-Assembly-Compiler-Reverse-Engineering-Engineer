#include <stdio.h>
static int transform(int x) {
    int doubled = x * 2;
    int constant = 40 + 2;
    return doubled + constant;
}
int main(void) {
    printf("%d\n", transform(5));
    return 0;
}

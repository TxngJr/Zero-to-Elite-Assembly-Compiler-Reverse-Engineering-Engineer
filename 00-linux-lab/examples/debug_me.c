#include <stdio.h>

static int add(int a, int b) {
    int result = a + b;
    return result;
}

int main(void) {
    int left = 20;
    int right = 22;
    int answer = add(left, right);
    printf("answer=%d\n", answer);
    return answer == 42 ? 0 : 1;
}

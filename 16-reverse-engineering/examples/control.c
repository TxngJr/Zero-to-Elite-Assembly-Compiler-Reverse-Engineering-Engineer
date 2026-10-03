#include <stdio.h>
#include <stdlib.h>

static int classify(int x) {
    switch (x) {
        case 0: return 11;
        case 1: return 23;
        case 2: return 37;
        case 5: return 91;
        default: return x * 3 + 7;
    }
}

int main(int argc, char **argv) {
    int x = argc > 1 ? atoi(argv[1]) : 2;
    printf("%d\n", classify(x));
    return 0;
}

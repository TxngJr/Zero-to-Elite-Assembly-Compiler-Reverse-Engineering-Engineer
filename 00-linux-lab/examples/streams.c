#include <stdio.h>

int main(void) {
    fputs("message on stdout\n", stdout);
    fputs("message on stderr\n", stderr);
    return 0;
}

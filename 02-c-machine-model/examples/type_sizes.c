#include <limits.h>
#include <stdio.h>

#define SHOW(T) printf("%-18s %zu bytes\n", #T, sizeof(T))
int main(void) {
    printf("CHAR_BIT           %d\n", CHAR_BIT);
    SHOW(char); SHOW(short); SHOW(int); SHOW(long); SHOW(long long); SHOW(void *); SHOW(size_t);
    return 0;
}

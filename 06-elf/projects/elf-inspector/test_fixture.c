#include <stdio.h>
int global_data = 9;
char global_bss[128];
int main(void) {
    global_bss[0] = 1;
    printf("%d\n", global_data + global_bss[0]);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
static int global_static = 1;
int global_external = 2;
int main(void) {
    static int local_static = 3;
    int automatic = 4;
    int *allocated = malloc(sizeof *allocated);
    if (!allocated) return 1;
    *allocated = 5;
    printf("global_static=%p global_external=%p local_static=%p automatic=%p allocated=%p\n",
           (void *)&global_static,(void *)&global_external,(void *)&local_static,(void *)&automatic,(void *)allocated);
    free(allocated);
    return 0;
}

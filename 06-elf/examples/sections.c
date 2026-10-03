#include <stdio.h>
const char course_name[] = "Zero to Elite";
int initialized_global = 7;
unsigned char zero_buffer[4096];
static int twice(int x) { return x * 2; }
int main(void) {
    zero_buffer[0] = (unsigned char)twice(initialized_global);
    printf("%s %u\n", course_name, (unsigned)zero_buffer[0]);
    return 0;
}

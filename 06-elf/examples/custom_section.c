#include <stdio.h>
__attribute__((section(".course_meta"), used))
const char course_meta[] = "chapter=06;format=ELF64";
int main(void) {
    puts(course_meta);
    return 0;
}

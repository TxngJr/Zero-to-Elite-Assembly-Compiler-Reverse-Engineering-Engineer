#include <stdio.h>
int main(void) {
    const unsigned char chars[]={'A','a','0',' ','\n'};
    for(size_t i=0;i<sizeof chars;++i) {
        printf("repr=%s decimal=%u hex=0x%02X\n",chars[i]=='\n'?"\\n":(char[2]){(char)chars[i],'\0'},(unsigned)chars[i],(unsigned)chars[i]);
    }
    return 0;
}

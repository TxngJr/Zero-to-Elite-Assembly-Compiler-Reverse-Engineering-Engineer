#include <stdint.h>
#include <stdio.h>
int main(void) {
    uint32_t value=UINT32_C(0x12345678);
    const unsigned char *bytes=(const unsigned char *)&value;
    printf("value=0x%08X bytes=",value);
    for(size_t i=0;i<sizeof value;++i) printf("%02X%s",bytes[i],i+1==sizeof value?"":" ");
    putchar('\n');
    if(bytes[0]==0x78u) puts("observed byte order: little-endian");
    else if(bytes[0]==0x12u) puts("observed byte order: big-endian");
    else puts("observed byte order: other/mixed representation");
    return 0;
}

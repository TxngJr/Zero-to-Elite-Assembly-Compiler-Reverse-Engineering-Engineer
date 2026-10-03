#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
static void view(const char *name,const void *object,size_t size){
    const unsigned char *p=object;
    printf("%-12s address=%p size=%zu bytes=",name,object,size);
    for(size_t i=0;i<size;++i)printf("%02X%s",p[i],i+1==size?"":" ");
    putchar('\n');
}
struct sample{uint8_t tag;uint32_t value;uint16_t code;};
int main(void){
    uint16_t u16=UINT16_C(0x1234);uint32_t u32=UINT32_C(0x12345678);uint64_t u64=UINT64_C(0x0123456789ABCDEF);
    struct sample s={0xAAu,UINT32_C(0x11223344),UINT16_C(0x5566)};
    view("uint16_t",&u16,sizeof u16);view("uint32_t",&u32,sizeof u32);view("uint64_t",&u64,sizeof u64);view("struct",&s,sizeof s);
    puts("Addresses above are process virtual addresses, not asserted physical RAM locations.");
    return 0;
}

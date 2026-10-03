#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
static void dump(const void *object,size_t size) {
    const unsigned char *p=object;
    printf("address=%p size=%zu bytes=",object,size);
    for(size_t i=0;i<size;++i) printf("%02X%s",p[i],i+1==size?"":" ");
    putchar('\n');
}
int main(void) {
    uint16_t a=UINT16_C(0x1234);
    uint32_t b=UINT32_C(0x12345678);
    uint64_t c=UINT64_C(0x0123456789ABCDEF);
    dump(&a,sizeof a); dump(&b,sizeof b); dump(&c,sizeof c);
    return 0;
}

#include <stdint.h>
#include <stdio.h>
enum { FLAG_READ=1u<<0, FLAG_WRITE=1u<<1, FLAG_EXEC=1u<<2, FLAG_ADMIN=1u<<3 };
int main(void) {
    uint8_t flags=0;
    flags |= FLAG_READ|FLAG_WRITE;
    printf("after set read/write: 0x%02X\n",(unsigned)flags);
    flags ^= FLAG_WRITE;
    printf("after toggle write:   0x%02X\n",(unsigned)flags);
    flags |= FLAG_ADMIN;
    printf("admin? %s\n",(flags&FLAG_ADMIN)!=0u?"yes":"no");
    flags &= (uint8_t)~FLAG_READ;
    printf("after clear read:     0x%02X\n",(unsigned)flags);
    return 0;
}

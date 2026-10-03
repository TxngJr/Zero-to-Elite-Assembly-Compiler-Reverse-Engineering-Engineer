#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
struct record { uint8_t tag; uint32_t value; uint16_t code; };
struct reordered { uint32_t value; uint16_t code; uint8_t tag; };
int main(void) {
    printf("record size=%zu offsets tag=%zu value=%zu code=%zu\n", sizeof(struct record), offsetof(struct record,tag), offsetof(struct record,value), offsetof(struct record,code));
    printf("reordered size=%zu offsets value=%zu code=%zu tag=%zu\n", sizeof(struct reordered), offsetof(struct reordered,value), offsetof(struct reordered,code), offsetof(struct reordered,tag));
    return 0;
}

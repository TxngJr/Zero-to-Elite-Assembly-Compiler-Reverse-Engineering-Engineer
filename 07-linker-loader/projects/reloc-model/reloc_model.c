#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void put_u64le(unsigned char *p, uint64_t v) {
    for (unsigned i = 0; i < 8; ++i) p[i] = (unsigned char)(v >> (8u * i));
}
static void put_u32le(unsigned char *p, uint32_t v) {
    for (unsigned i = 0; i < 4; ++i) p[i] = (unsigned char)(v >> (8u * i));
}
static uint64_t get_u64le(const unsigned char *p) {
    uint64_t v = 0;
    for (unsigned i = 0; i < 8; ++i) v |= (uint64_t)p[i] << (8u * i);
    return v;
}
static uint32_t get_u32le(const unsigned char *p) {
    uint32_t v = 0;
    for (unsigned i = 0; i < 4; ++i) v |= (uint32_t)p[i] << (8u * i);
    return v;
}
int main(void) {
    unsigned char image[16];
    memset(image, 0, sizeof image);

    const uint64_t S = UINT64_C(0x401000);
    const int64_t A_abs = 8;
    const uint64_t abs_value = (uint64_t)((int64_t)S + A_abs);
    put_u64le(image, abs_value);

    const int64_t A_pc = -4;
    const uint64_t P = UINT64_C(0x400100);
    const int64_t pc_value = (int64_t)S + A_pc - (int64_t)P;
    if (pc_value < INT32_MIN || pc_value > INT32_MAX) {
        fputs("PC32 overflow\n", stderr);
        return 1;
    }
    put_u32le(image + 8, (uint32_t)(int32_t)pc_value);

    printf("ABS64=0x%" PRIx64 "\n", get_u64le(image));
    printf("PC32=%" PRId32 "\n", (int32_t)get_u32le(image + 8));
    return 0;
}

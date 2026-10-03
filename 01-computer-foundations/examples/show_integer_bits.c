#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void print_bits_u64(uint64_t value, unsigned width) {
    for (unsigned i = width; i > 0; --i) {
        unsigned shift = i - 1;
        putchar((value & (UINT64_C(1) << shift)) ? '1' : '0');
    }
}
int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: %s NUMBER\n", argv[0]); return 2; }
    char *end = NULL;
    unsigned long long raw = strtoull(argv[1], &end, 0);
    if (end == argv[1] || *end != '\0') { fputs("invalid integer\n", stderr); return 2; }
    uint64_t value = (uint64_t)raw;
    printf("decimal: %" PRIu64 "\nhex: 0x%016" PRIX64 "\nbinary: ", value, value);
    print_bits_u64(value, 64);
    putchar('\n');
    return 0;
}

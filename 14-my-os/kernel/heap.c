#include "heap.h"

static unsigned char heap_area[64 * 1024] __attribute__((aligned(16)));
static size_t offset;

void heap_init(void) {
    offset = 0;
}

void *kmalloc(size_t size) {
    if (size == 0) {
        size = 1;
    }

    size = (size + 15u) & ~(size_t)15u;

    if (size > sizeof heap_area - offset) {
        return 0;
    }

    void *result = &heap_area[offset];
    offset += size;
    return result;
}

size_t heap_used(void) {
    return offset;
}

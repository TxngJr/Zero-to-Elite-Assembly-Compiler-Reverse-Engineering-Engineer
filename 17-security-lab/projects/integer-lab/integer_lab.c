#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

static int checked_add_size(size_t a, size_t b, size_t *out) {
    if (a > SIZE_MAX - b) {
        return 0;
    }
    *out = a + b;
    return 1;
}

static int checked_mul_size(size_t a, size_t b, size_t *out) {
    if (a != 0 && b > SIZE_MAX / a) {
        return 0;
    }
    *out = a * b;
    return 1;
}

int main(void) {
    size_t out = 0;

    assert(checked_add_size(10, 20, &out) && out == 30);
    assert(!checked_add_size(SIZE_MAX, 1, &out));
    assert(checked_mul_size(8, 16, &out) && out == 128);
    assert(!checked_mul_size(SIZE_MAX, 2, &out));
    assert(checked_mul_size(0, SIZE_MAX, &out) && out == 0);

    puts("integer-lab: OK");
    return 0;
}

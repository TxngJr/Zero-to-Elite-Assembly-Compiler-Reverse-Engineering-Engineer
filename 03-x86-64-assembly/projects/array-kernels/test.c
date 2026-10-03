#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
long long asm_sum_i64(const long long *a, size_t n);
long long asm_max_i64(const long long *a, size_t n);
uint64_t asm_xor_reduce_u64(const uint64_t *a, size_t n);
int main(void) {
    const long long a[] = {7, -2, 40, 1, -9};
    const uint64_t b[] = {UINT64_C(0xAA), UINT64_C(0x0F), UINT64_C(0x55)};
    assert(asm_sum_i64(a, 5) == 37);
    assert(asm_max_i64(a, 5) == 40);
    assert(asm_max_i64(a, 0) == 0);
    assert(asm_xor_reduce_u64(b, 3) == (UINT64_C(0xAA) ^ UINT64_C(0x0F) ^ UINT64_C(0x55)));
    puts("array-kernels: OK");
    return 0;
}

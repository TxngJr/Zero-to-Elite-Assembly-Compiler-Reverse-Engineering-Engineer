#include <stdint.h>
#include <stdio.h>

typedef struct {
    uint32_t id;
    uint16_t flags;
    uint16_t count;
    int64_t value;
} Record;

static long long sum_records(const Record *records, size_t n) {
    long long total = 0;
    for (size_t i = 0; i < n; ++i) {
        if ((records[i].flags & 1u) != 0u) {
            total += records[i].value * records[i].count;
        }
    }
    return total;
}

int main(void) {
    const Record records[] = {
        {1, 1, 2, 10},
        {2, 0, 4, 20},
        {3, 1, 3, -5},
    };
    printf("%lld\n", sum_records(records, 3));
    return 0;
}

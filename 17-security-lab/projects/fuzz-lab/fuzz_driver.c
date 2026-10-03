#include "../parser-lab/parser.h"

#include <assert.h>
#include <stdint.h>
#include <stdio.h>

static uint32_t state = UINT32_C(0xC0FFEE01);

static uint32_t next_u32(void) {
    state = state * UINT32_C(1664525) + UINT32_C(1013904223);
    return state;
}

int main(void) {
    Packet packet;
    uint8_t input[32];

    for (unsigned iteration = 0; iteration < 5000; ++iteration) {
        const size_t size = (size_t)(next_u32() % (sizeof input + 1));

        for (size_t i = 0; i < size; ++i) {
            input[i] = (uint8_t)next_u32();
        }

        (void)parse_packet(input, size, &packet);
    }

    const uint8_t valid[] = {1, 7, 7};
    assert(parse_packet(valid, sizeof valid, &packet));

    puts("fuzz-lab: 5000 deterministic cases OK");
    return 0;
}

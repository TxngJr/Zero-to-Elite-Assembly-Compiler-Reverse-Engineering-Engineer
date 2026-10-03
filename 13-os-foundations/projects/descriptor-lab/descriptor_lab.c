#include <assert.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

typedef struct __attribute__((packed)) {
    uint16_t offset_low;
    uint16_t selector;
    uint8_t ist;
    uint8_t attributes;
    uint16_t offset_mid;
    uint32_t offset_high;
    uint32_t zero;
} IdtGate;

static IdtGate make_gate(uint64_t address, uint16_t selector, uint8_t attributes) {
    IdtGate gate = {
        .offset_low = (uint16_t)address,
        .selector = selector,
        .ist = 0,
        .attributes = attributes,
        .offset_mid = (uint16_t)(address >> 16),
        .offset_high = (uint32_t)(address >> 32),
        .zero = 0,
    };
    return gate;
}

static uint64_t gate_address(const IdtGate *gate) {
    return (uint64_t)gate->offset_low |
           ((uint64_t)gate->offset_mid << 16) |
           ((uint64_t)gate->offset_high << 32);
}

int main(void) {
    const uint64_t expected = UINT64_C(0x1122334455667788);
    IdtGate gate = make_gate(expected, 0x08, 0x8E);

    assert(sizeof(IdtGate) == 16);
    assert(gate_address(&gate) == expected);
    assert(gate.selector == 0x08);
    assert(gate.attributes == 0x8E);

    printf("idt_gate=%zu handler=0x%016" PRIx64
           " selector=0x%04x attr=0x%02x\n",
           sizeof gate, gate_address(&gate),
           gate.selector, gate.attributes);
    return 0;
}

#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { OP_HALT, OP_MOVI, OP_ADD, OP_SUB, OP_LOAD, OP_STORE, OP_JZ, OP_JMP };

typedef struct {
    uint16_t r[4];
    uint16_t pc;
    uint16_t mem[256];
    int halted;
} Cpu;

static uint16_t enc(unsigned op, unsigned a, unsigned b) {
    return (uint16_t)(((op & 0xFu) << 12) | ((a & 0x3u) << 10) | (b & 0x3FFu));
}

static int step(Cpu *c, const uint16_t *program, size_t words) {
    if (c->halted || c->pc >= words) {
        return 0;
    }

    uint16_t ins = program[c->pc++];
    unsigned op = ins >> 12;
    unsigned a = (ins >> 10) & 3u;
    unsigned b = ins & 0x3FFu;

    switch (op) {
        case OP_HALT: c->halted = 1; break;
        case OP_MOVI: c->r[a] = (uint16_t)b; break;
        case OP_ADD: c->r[a] = (uint16_t)(c->r[a] + c->r[b & 3u]); break;
        case OP_SUB: c->r[a] = (uint16_t)(c->r[a] - c->r[b & 3u]); break;
        case OP_LOAD: c->r[a] = c->mem[b & 0xFFu]; break;
        case OP_STORE: c->mem[b & 0xFFu] = c->r[a]; break;
        case OP_JZ:
            if (c->r[a] == 0) c->pc = (uint16_t)b;
            break;
        case OP_JMP: c->pc = (uint16_t)b; break;
        default: return 0;
    }
    return 1;
}

static int run(Cpu *c, const uint16_t *program, size_t words, unsigned limit) {
    for (unsigned i = 0; i < limit && !c->halted; ++i) {
        if (!step(c, program, words)) return 0;
    }
    return c->halted;
}

int main(void) {
    const uint16_t program[] = {
        enc(OP_MOVI, 0, 10),
        enc(OP_MOVI, 1, 20),
        enc(OP_ADD, 0, 1),
        enc(OP_STORE, 0, 5),
        enc(OP_HALT, 0, 0)
    };
    Cpu c;
    memset(&c, 0, sizeof c);
    if (!run(&c, program, sizeof program / sizeof program[0], 100)) return 1;
    printf("r0=%u mem[5]=%u pc=%u\n", c.r[0], c.mem[5], c.pc);
    return c.mem[5] == 30 ? 0 : 1;
}

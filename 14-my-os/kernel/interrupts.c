#include "interrupts.h"
#include "console.h"
#include "ports.h"

#include <stdint.h>

typedef struct __attribute__((packed)) {
    uint16_t offset_low;
    uint16_t selector;
    uint8_t ist;
    uint8_t attributes;
    uint16_t offset_mid;
    uint32_t offset_high;
    uint32_t zero;
} IdtGate;

typedef struct __attribute__((packed)) {
    uint16_t limit;
    uint64_t base;
} Idtr;

static IdtGate idt[256];

extern void isr_default(void);
extern void exception_de_stub(void);
extern void exception_ud_stub(void);
extern void exception_gp_stub(void);
extern void exception_pf_stub(void);
extern void irq0_stub(void);
extern void irq1_stub(void);

static void set_gate(unsigned vector, void (*handler)(void)) {
    const uint64_t address = (uint64_t)(uintptr_t)handler;
    idt[vector] = (IdtGate){
        .offset_low = (uint16_t)address,
        .selector = 0x08,
        .ist = 0,
        .attributes = 0x8E,
        .offset_mid = (uint16_t)(address >> 16),
        .offset_high = (uint32_t)(address >> 32),
        .zero = 0,
    };
}

static void pic_remap(void) {
    const uint8_t mask1 = inb(0x21);
    const uint8_t mask2 = inb(0xA1);

    outb(0x20, 0x11); io_wait();
    outb(0xA0, 0x11); io_wait();
    outb(0x21, 0x20); io_wait();
    outb(0xA1, 0x28); io_wait();
    outb(0x21, 0x04); io_wait();
    outb(0xA1, 0x02); io_wait();
    outb(0x21, 0x01); io_wait();
    outb(0xA1, 0x01); io_wait();

    outb(0x21, mask1);
    outb(0xA1, mask2);
}

void interrupts_init(void) {
    for (unsigned i = 0; i < 256; ++i) {
        set_gate(i, isr_default);
    }

    /* Common faults get diagnostic stubs instead of a silent halt. */
    set_gate(0, exception_de_stub);
    set_gate(6, exception_ud_stub);
    set_gate(13, exception_gp_stub);
    set_gate(14, exception_pf_stub);

    set_gate(32, irq0_stub);
    set_gate(33, irq1_stub);

    const Idtr pointer = {
        .limit = (uint16_t)(sizeof idt - 1),
        .base = (uint64_t)(uintptr_t)idt,
    };
    __asm__ volatile("lidt %0" : : "m"(pointer));

    pic_remap();

    /* Enable only PIT timer (IRQ0) and PS/2 keyboard (IRQ1). */
    outb(0x21, 0xFC);
    outb(0xA1, 0xFF);
}

void interrupts_enable(void) {
    __asm__ volatile("sti");
}

void pit_init(uint32_t hz) {
    if (hz < 19) {
        hz = 19;
    }
    if (hz > 1000) {
        hz = 1000;
    }

    const uint32_t divisor = 1193182u / hz;
    outb(0x43, 0x36);
    outb(0x40, (uint8_t)divisor);
    outb(0x40, (uint8_t)(divisor >> 8));
}

__attribute__((noreturn))
void exception_panic(uint64_t vector, uint64_t error_code, uint64_t rip) {
    console_write("\n[EXCEPTION] vector=");
    console_write_dec(vector);
    console_write(" error=");
    console_write_hex(error_code);
    console_write(" rip=");
    console_write_hex(rip);

    if (vector == 14) {
        uint64_t cr2;
        __asm__ volatile("mov %%cr2, %0" : "=r"(cr2));
        console_write(" cr2=");
        console_write_hex(cr2);
    }

    console_putc('\n');
    console_write("[EXCEPTION] kernel halted\n");

    for (;;) {
        __asm__ volatile("cli; hlt");
    }
}

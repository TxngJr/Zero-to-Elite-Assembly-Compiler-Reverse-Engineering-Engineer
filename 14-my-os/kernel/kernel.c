#include "console.h"
#include "heap.h"
#include "interrupts.h"
#include "pmm.h"
#include "shell.h"

#include <stdint.h>

#define MULTIBOOT2_BOOT_MAGIC UINT32_C(0x36D76289)

static void halt_forever(void) {
    for (;;) {
        __asm__ volatile("cli; hlt");
    }
}

void kernel_main(uint32_t magic, uint32_t info) {
    console_init();
    console_write("EliteOS64 booted\n");
    console_write("[BOOT] console ok\n");

    if (magic != MULTIBOOT2_BOOT_MAGIC) {
        console_write("[BOOT] bad multiboot2 magic\n");
        halt_forever();
    }

    console_write("multiboot2 info=");
    console_write_hex(info);
    console_putc('\n');

    pmm_init((uintptr_t)info);
    heap_init();

    console_write("free frames below 4GiB=");
    console_write_dec(pmm_free_frames());
    console_putc('\n');
    console_write("[BOOT] pmm/heap ok\n");

    interrupts_init();
    pit_init(100);
    console_write("[BOOT] idt/pic/pit configured\n");

    interrupts_enable();

    /*
     * Wait for real PIT interrupts before claiming the timer path works.
     * This turns the QEMU smoke test into a runtime interrupt test rather
     * than a static-symbol check.
     */
    while (timer_ticks < 3) {
        __asm__ volatile("hlt");
    }
    console_write("[BOOT] pit irq ok\n");

    shell_init();
    console_write("[BOOT] shell ready (serial + ps2 input)\n");

    for (;;) {
        __asm__ volatile("hlt");

        const uint8_t scancode = last_scancode;
        if (scancode != 0) {
            last_scancode = 0;
            shell_feed_scancode(scancode);
        }

        char serial_char;
        while (console_try_read(&serial_char)) {
            shell_feed_char(serial_char);
        }
    }
}

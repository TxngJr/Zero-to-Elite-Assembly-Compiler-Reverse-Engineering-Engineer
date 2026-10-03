#include "console.h"
#include "heap.h"
#include "interrupts.h"
#include "pmm.h"
#include "shell.h"

#include <stdint.h>

#define MULTIBOOT2_BOOT_MAGIC UINT32_C(0x36D76289)

void kernel_main(uint32_t magic, uint32_t info) {
    console_init();
    console_write("EliteOS64 booted\n");

    if (magic != MULTIBOOT2_BOOT_MAGIC) {
        console_write("bad multiboot2 magic\n");
        for (;;) {
            __asm__ volatile("cli; hlt");
        }
    }

    console_write("multiboot2 info=");
    console_write_hex(info);
    console_putc('\n');

    pmm_init((uintptr_t)info);
    heap_init();

    console_write("free frames below 4GiB=");
    console_write_dec(pmm_free_frames());
    console_putc('\n');

    interrupts_init();
    pit_init(100);
    shell_init();
    interrupts_enable();

    for (;;) {
        __asm__ volatile("hlt");

        const uint8_t scancode = last_scancode;
        if (scancode != 0) {
            last_scancode = 0;
            shell_feed_scancode(scancode);
        }
    }
}

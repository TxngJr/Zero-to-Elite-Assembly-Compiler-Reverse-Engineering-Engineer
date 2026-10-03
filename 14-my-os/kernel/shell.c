#include "shell.h"

#include "console.h"
#include "heap.h"
#include "interrupts.h"
#include "pmm.h"

#include <stddef.h>
#include <stdint.h>

static char line[64];
static size_t length;

static int equal(const char *a, const char *b) {
    while (*a != '\0' && *a == *b) {
        ++a;
        ++b;
    }
    return *a == *b;
}

static void prompt(void) {
    console_write("elite> ");
}

static void run_command(void) {
    line[length] = '\0';

    if (equal(line, "help")) {
        console_write("help ticks mem alloc clear\n");
    } else if (equal(line, "ticks")) {
        console_write("ticks=");
        console_write_dec(timer_ticks);
        console_putc('\n');
    } else if (equal(line, "mem")) {
        console_write("frames=");
        console_write_dec(pmm_free_frames());
        console_write(" heap=");
        console_write_dec(heap_used());
        console_putc('\n');
    } else if (equal(line, "alloc")) {
        const uintptr_t frame = pmm_alloc_frame();
        console_write("frame=");
        console_write_hex(frame);
        console_putc('\n');
    } else if (equal(line, "clear")) {
        console_clear();
    } else if (length != 0) {
        console_write("unknown command\n");
    }

    length = 0;
    prompt();
}

static char translate(uint8_t scancode) {
    static const char map[58] = {
        0, 0, '1', '2', '3', '4', '5', '6',
        '7', '8', '9', '0', '-', '=', 0, 0,
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i',
        'o', 'p', '[', ']', 0, 0, 'a', 's',
        'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
        39, 96, 0, '\\', 'z', 'x', 'c', 'v',
        'b', 'n', 'm', ',', '.', '/', 0, '*',
        0, ' '
    };

    return scancode < 58 ? map[scancode] : 0;
}

void shell_init(void) {
    length = 0;
    console_write("commands: help ticks mem alloc clear\n");
    prompt();
}

void shell_feed_scancode(uint8_t scancode) {
    if ((scancode & 0x80u) != 0u) {
        return;
    }

    if (scancode == 0x1C) {
        console_putc('\n');
        run_command();
        return;
    }

    if (scancode == 0x0E) {
        if (length != 0) {
            --length;
            console_putc('\b');
        }
        return;
    }

    const char c = translate(scancode);
    if (c != 0 && length + 1 < sizeof line) {
        line[length++] = c;
        console_putc(c);
    }
}

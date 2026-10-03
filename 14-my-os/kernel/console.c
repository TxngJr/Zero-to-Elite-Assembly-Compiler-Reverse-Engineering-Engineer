#include "console.h"
#include "ports.h"

#include <stddef.h>
#include <stdint.h>

static volatile uint16_t *const VGA = (uint16_t *)0xB8000;
static size_t row;
static size_t column;
static uint8_t attribute = 0x0F;

static uint16_t cell(char c) {
    return (uint16_t)(((uint16_t)attribute << 8) | (uint8_t)c);
}

static void serial_init(void) {
    outb(0x3F9, 0x00);
    outb(0x3FB, 0x80);
    outb(0x3F8, 0x03);
    outb(0x3F9, 0x00);
    outb(0x3FB, 0x03);
    outb(0x3FA, 0xC7);
    outb(0x3FC, 0x0B);
}

static void serial_putc(char c) {
    while ((inb(0x3FD) & 0x20u) == 0u) {
    }
    outb(0x3F8, (uint8_t)c);
}

static void scroll(void) {
    if (row < 25) {
        return;
    }
    for (size_t r = 1; r < 25; ++r) {
        for (size_t c = 0; c < 80; ++c) {
            VGA[(r - 1) * 80 + c] = VGA[r * 80 + c];
        }
    }
    for (size_t c = 0; c < 80; ++c) {
        VGA[24 * 80 + c] = cell(' ');
    }
    row = 24;
}

void console_clear(void) {
    for (size_t i = 0; i < 80 * 25; ++i) {
        VGA[i] = cell(' ');
    }
    row = 0;
    column = 0;
}

void console_init(void) {
    serial_init();
    console_clear();
}

void console_putc(char c) {
    serial_putc(c);

    if (c == '\n') {
        column = 0;
        ++row;
        scroll();
        return;
    }

    if (c == '\b') {
        if (column != 0) {
            --column;
            VGA[row * 80 + column] = cell(' ');
        }
        return;
    }

    VGA[row * 80 + column] = cell(c);
    ++column;
    if (column >= 80) {
        column = 0;
        ++row;
        scroll();
    }
}

void console_write(const char *s) {
    while (*s != '\0') {
        console_putc(*s++);
    }
}

void console_write_hex(uint64_t value) {
    static const char digits[] = "0123456789abcdef";
    console_write("0x");
    for (int i = 15; i >= 0; --i) {
        console_putc(digits[(value >> ((unsigned)i * 4u)) & 0xFu]);
    }
}

void console_write_dec(uint64_t value) {
    char buffer[21];
    size_t length = 0;

    if (value == 0) {
        console_putc('0');
        return;
    }

    while (value != 0) {
        buffer[length++] = (char)('0' + value % 10u);
        value /= 10u;
    }

    while (length != 0) {
        console_putc(buffer[--length]);
    }
}

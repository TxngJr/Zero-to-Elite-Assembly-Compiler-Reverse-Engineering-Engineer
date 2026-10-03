#ifndef ELITEOS_CONSOLE_H
#define ELITEOS_CONSOLE_H

#include <stdint.h>

void console_init(void);
void console_clear(void);
void console_putc(char c);
void console_write(const char *s);
void console_write_hex(uint64_t value);
void console_write_dec(uint64_t value);

#endif

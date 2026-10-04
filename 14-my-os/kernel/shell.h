#ifndef ELITEOS_SHELL_H
#define ELITEOS_SHELL_H

#include <stdint.h>

void shell_init(void);
void shell_feed_char(char c);
void shell_feed_scancode(uint8_t scancode);

#endif

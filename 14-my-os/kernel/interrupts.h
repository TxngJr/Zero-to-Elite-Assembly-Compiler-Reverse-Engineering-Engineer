#ifndef ELITEOS_INTERRUPTS_H
#define ELITEOS_INTERRUPTS_H

#include <stdint.h>

extern volatile uint64_t timer_ticks;
extern volatile uint8_t last_scancode;

void interrupts_init(void);
void interrupts_enable(void);
void pit_init(uint32_t hz);

#endif

#ifndef ELITEOS_HEAP_H
#define ELITEOS_HEAP_H

#include <stddef.h>

void heap_init(void);
void *kmalloc(size_t size);
size_t heap_used(void);

#endif

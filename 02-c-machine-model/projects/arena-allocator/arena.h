#ifndef ARENA_H
#define ARENA_H
#include <stddef.h>
typedef struct { unsigned char *base; size_t capacity; size_t offset; } Arena;
int arena_init(Arena *a, size_t capacity);
void arena_destroy(Arena *a);
void arena_reset(Arena *a);
void *arena_alloc(Arena *a, size_t size, size_t alignment);
#endif

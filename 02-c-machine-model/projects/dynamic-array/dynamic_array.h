#ifndef DYNAMIC_ARRAY_H
#define DYNAMIC_ARRAY_H
#include <stddef.h>
typedef struct { int *data; size_t length; size_t capacity; } IntVector;
void iv_init(IntVector *v);
void iv_destroy(IntVector *v);
int iv_reserve(IntVector *v, size_t capacity);
int iv_push(IntVector *v, int value);
int iv_get(const IntVector *v, size_t index, int *out);
int iv_set(IntVector *v, size_t index, int value);
int iv_resize(IntVector *v, size_t length, int fill);
#endif

#ifndef MINI_STRING_H
#define MINI_STRING_H
#include <stddef.h>
size_t zs_length(const char *s);
int zs_compare(const char *a, const char *b);
int zs_copy(char *dst, size_t capacity, const char *src);
const char *zs_find_char(const char *s, char needle);
void zs_reverse(char *s);
#endif

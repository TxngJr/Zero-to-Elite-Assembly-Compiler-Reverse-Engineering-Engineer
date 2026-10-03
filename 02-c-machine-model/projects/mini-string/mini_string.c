#include "mini_string.h"

size_t zs_length(const char *s) {
    size_t n = 0;
    while (s[n] != '\0') ++n;
    return n;
}
int zs_compare(const char *a, const char *b) {
    size_t i = 0;
    while (a[i] != '\0' && a[i] == b[i]) ++i;
    return (unsigned char)a[i] < (unsigned char)b[i] ? -1 :
           (unsigned char)a[i] > (unsigned char)b[i] ? 1 : 0;
}
int zs_copy(char *dst, size_t capacity, const char *src) {
    size_t n = zs_length(src);
    if (capacity == 0 || n >= capacity) return 0;
    for (size_t i = 0; i <= n; ++i) dst[i] = src[i];
    return 1;
}
const char *zs_find_char(const char *s, char needle) {
    for (size_t i = 0;; ++i) {
        if (s[i] == needle) return &s[i];
        if (s[i] == '\0') return NULL;
    }
}
void zs_reverse(char *s) {
    size_t n = zs_length(s);
    for (size_t i = 0; i < n / 2; ++i) {
        char t = s[i]; s[i] = s[n - 1 - i]; s[n - 1 - i] = t;
    }
}

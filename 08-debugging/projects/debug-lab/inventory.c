#include "inventory.h"

void inventory_init(Inventory *inv) {
    inv->count = 0;
}
int inventory_push(Inventory *inv, int value) {
#ifdef INJECT_BUG
    if (inv->count > 8) return 0; /* Intentional off-by-one for sanitizer/GDB lab. */
#else
    if (inv->count >= 8) return 0;
#endif
    inv->items[inv->count++] = value;
    return 1;
}
long inventory_total(const Inventory *inv) {
    long total = 0;
    for (size_t i = 0; i < inv->count; ++i) total += inv->items[i];
    return total;
}

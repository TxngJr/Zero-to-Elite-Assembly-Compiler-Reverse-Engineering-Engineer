#ifndef INVENTORY_H
#define INVENTORY_H
#include <stddef.h>
typedef struct {
    int items[8];
    size_t count;
} Inventory;
void inventory_init(Inventory *inv);
int inventory_push(Inventory *inv, int value);
long inventory_total(const Inventory *inv);
#endif

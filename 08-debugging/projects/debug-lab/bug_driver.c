#include "inventory.h"
#include <stdio.h>
int main(void) {
    Inventory inv;
    inventory_init(&inv);
    for (int i = 0; i < 9; ++i) {
        if (!inventory_push(&inv, 100 + i)) break;
    }
    printf("count=%zu total=%ld\n", inv.count, inventory_total(&inv));
    return 0;
}

#include "inventory.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    Inventory inv;
    inventory_init(&inv);
    for (int i = 1; i <= 8; ++i) assert(inventory_push(&inv, i));
    assert(!inventory_push(&inv, 99));
    assert(inv.count == 8);
    assert(inventory_total(&inv) == 36);
    puts("debug-lab: OK");
    return 0;
}

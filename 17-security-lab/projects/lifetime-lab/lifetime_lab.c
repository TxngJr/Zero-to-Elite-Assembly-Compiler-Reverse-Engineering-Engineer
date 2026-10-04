#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int value;
} Box;

int main(void) {
    Box *box = malloc(sizeof *box);
    if (!box) {
        return 2;
    }

    box->value = 42;
    assert(box->value == 42);

#ifdef INJECT_UAF
    free(box);
    /*
     * Intentional course-only lifetime defect for AddressSanitizer.
     * The lab is to identify/fix ownership, not to exploit the bug.
     */
    volatile int observed = box->value;
    (void)observed;
#else
    const int observed = box->value;
    free(box);
    assert(observed == 42);
#endif

    puts("lifetime-lab: OK");
    return 0;
}

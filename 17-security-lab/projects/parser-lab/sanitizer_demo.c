#include "parser.h"

#include <stdint.h>

int main(void) {
    Packet packet;
    uint8_t malformed[20] = {0};
    malformed[0] = 19;

    for (unsigned i = 1; i < sizeof malformed; ++i) {
        malformed[i] = (uint8_t)i;
    }

    /*
     * In INJECT_BUG builds this intentionally reaches an invalid copy.
     * The lab goal is sanitizer/root-cause practice only.
     */
    (void)parse_packet(malformed, sizeof malformed, &packet);
    return 0;
}

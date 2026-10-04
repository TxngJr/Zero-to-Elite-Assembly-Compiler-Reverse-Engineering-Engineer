#include "../parser-lab/parser.h"

#include <stddef.h>
#include <stdint.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Packet packet;
    (void)parse_packet(data, size, &packet);
    return 0;
}

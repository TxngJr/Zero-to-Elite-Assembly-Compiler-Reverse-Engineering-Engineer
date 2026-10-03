#include "parser.h"

#include <string.h>

int parse_packet(const uint8_t *data, size_t size, Packet *out) {
    if (!data || !out || size < 2) {
        return 0;
    }

    const size_t claimed = data[0];

#ifndef INJECT_BUG
    if (claimed > PAYLOAD_MAX) {
        return 0;
    }
    if (claimed > size - 2) {
        return 0;
    }
#else
    /*
     * Intentional course-only defect:
     * length validation is omitted so sanitizers can demonstrate
     * how an invalid copy is detected. Do not use this build outside
     * the local lab.
     */
#endif

    Packet temp = {0};
    temp.length = (uint8_t)claimed;
    memcpy(temp.payload, data + 1, claimed);
    temp.checksum = data[1 + claimed];

    unsigned sum = 0;
    for (size_t i = 0; i < claimed; ++i) {
        sum = (sum + temp.payload[i]) & 0xFFu;
    }
    if ((uint8_t)sum != temp.checksum) {
        return 0;
    }

    *out = temp;
    return 1;
}

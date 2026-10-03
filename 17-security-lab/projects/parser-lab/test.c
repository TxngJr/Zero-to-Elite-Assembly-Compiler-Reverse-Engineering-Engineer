#include "parser.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    Packet packet;

    const uint8_t good[] = {3, 'a', 'b', 'c', (uint8_t)('a' + 'b' + 'c')};
    assert(parse_packet(good, sizeof good, &packet));
    assert(packet.length == 3);
    assert(memcmp(packet.payload, "abc", 3) == 0);

    const uint8_t truncated[] = {4, 'a', 'b', 0};
    assert(!parse_packet(truncated, sizeof truncated, &packet));

    uint8_t oversized[PAYLOAD_MAX + 3] = {0};
    oversized[0] = PAYLOAD_MAX + 1;
    assert(!parse_packet(oversized, sizeof oversized, &packet));

    const uint8_t bad_checksum[] = {2, 1, 2, 99};
    assert(!parse_packet(bad_checksum, sizeof bad_checksum, &packet));

    assert(!parse_packet(NULL, 0, &packet));
    assert(!parse_packet(good, sizeof good, NULL));

    puts("parser-lab: OK");
    return 0;
}

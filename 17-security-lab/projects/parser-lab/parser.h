#ifndef SECURITY_LAB_PARSER_H
#define SECURITY_LAB_PARSER_H

#include <stddef.h>
#include <stdint.h>

#define PAYLOAD_MAX 16

typedef struct {
    uint8_t length;
    uint8_t payload[PAYLOAD_MAX];
    uint8_t checksum;
} Packet;

int parse_packet(const uint8_t *data, size_t size, Packet *out);

#endif

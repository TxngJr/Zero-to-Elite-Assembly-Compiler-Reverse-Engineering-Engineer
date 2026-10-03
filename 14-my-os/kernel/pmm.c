#include "pmm.h"

#include <stdint.h>

extern unsigned char kernel_end[];

typedef struct __attribute__((packed)) {
    uint32_t type;
    uint32_t size;
} Tag;

typedef struct __attribute__((packed)) {
    uint64_t address;
    uint64_t length;
    uint32_t type;
    uint32_t reserved;
} MemoryMapEntry;

typedef struct __attribute__((packed)) {
    uint32_t type;
    uint32_t size;
    uint32_t entry_size;
    uint32_t entry_version;
    MemoryMapEntry entries[];
} MemoryMapTag;

static uintptr_t next_frame;
static uintptr_t end_frame;

static uintptr_t align_up(uintptr_t value, uintptr_t alignment) {
    return (value + alignment - 1u) & ~(alignment - 1u);
}

void pmm_init(uintptr_t mbi) {
    static const uint64_t identity_limit = UINT64_C(0x100000000);

    next_frame = 0;
    end_frame = 0;

    const uint32_t total_size = *(const uint32_t *)mbi;
    const uintptr_t info_end = align_up(mbi + total_size, 4096);
    const uintptr_t kernel_limit = align_up((uintptr_t)kernel_end, 4096);
    const uintptr_t safe_start = info_end > kernel_limit ? info_end : kernel_limit;
    const uintptr_t tags_end = mbi + total_size;

    for (uintptr_t cursor = mbi + 8; cursor + sizeof(Tag) <= tags_end;) {
        const Tag *tag = (const Tag *)cursor;

        if (tag->type == 0) {
            break;
        }
        if (tag->size < sizeof(Tag) || cursor + tag->size > tags_end) {
            break;
        }

        if (tag->type == 6) {
            const MemoryMapTag *map = (const MemoryMapTag *)cursor;
            if (map->entry_size < sizeof(MemoryMapEntry)) {
                break;
            }

            uintptr_t entry_cursor = (uintptr_t)map->entries;
            const uintptr_t map_end = cursor + map->size;

            while (entry_cursor + sizeof(MemoryMapEntry) <= map_end) {
                const MemoryMapEntry *entry = (const MemoryMapEntry *)entry_cursor;

                if (entry->type == 1 && entry->address < identity_limit) {
                    uint64_t raw_end;
                    if (entry->length > UINT64_MAX - entry->address) {
                        raw_end = UINT64_MAX;
                    } else {
                        raw_end = entry->address + entry->length;
                    }

                    if (raw_end > identity_limit) {
                        raw_end = identity_limit;
                    }

                    uintptr_t start = (uintptr_t)entry->address;
                    uintptr_t end = (uintptr_t)raw_end;

                    if (start < safe_start) {
                        start = safe_start;
                    }
                    start = align_up(start, 4096);
                    end &= ~(uintptr_t)4095;

                    if (start < end) {
                        next_frame = start;
                        end_frame = end;
                        return;
                    }
                }

                entry_cursor += map->entry_size;
            }
        }

        cursor = align_up(cursor + tag->size, 8);
    }
}

uintptr_t pmm_alloc_frame(void) {
    if (next_frame == 0 || next_frame >= end_frame) {
        return 0;
    }

    const uintptr_t frame = next_frame;
    next_frame += 4096;
    return frame;
}

uint64_t pmm_free_frames(void) {
    if (next_frame == 0 || end_frame <= next_frame) {
        return 0;
    }
    return (end_frame - next_frame) / 4096;
}

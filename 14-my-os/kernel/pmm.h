#ifndef ELITEOS_PMM_H
#define ELITEOS_PMM_H

#include <stdint.h>

void pmm_init(uintptr_t multiboot_info);
uintptr_t pmm_alloc_frame(void);
uint64_t pmm_free_frames(void);

#endif

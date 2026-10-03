#include "arena.h"
#include <stdint.h>
#include <stdlib.h>
static int power_of_two(size_t x){return x!=0 && (x&(x-1))==0;}
int arena_init(Arena *a,size_t capacity){a->base=capacity?malloc(capacity):NULL;a->capacity=capacity;a->offset=0;return capacity==0||a->base!=NULL;}
void arena_destroy(Arena *a){free(a->base);a->base=NULL;a->capacity=0;a->offset=0;}
void arena_reset(Arena *a){a->offset=0;}
void *arena_alloc(Arena *a,size_t size,size_t alignment){
    if(!power_of_two(alignment)) return NULL;
    if(size==0) size=1;
    uintptr_t current=(uintptr_t)a->base + a->offset;
    uintptr_t mask=(uintptr_t)alignment-1u;
    if(current > UINTPTR_MAX - mask) return NULL;
    uintptr_t aligned=(current+mask)&~mask;
    if(aligned < (uintptr_t)a->base) return NULL;
    size_t start=(size_t)(aligned-(uintptr_t)a->base);
    if(start>a->capacity || size>a->capacity-start) return NULL;
    a->offset=start+size;
    return (void *)aligned;
}

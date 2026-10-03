#include "arena.h"
#include <assert.h>
#include <stdint.h>
int main(void){
    Arena a; assert(arena_init(&a,128));
    void *p1=arena_alloc(&a,1,1); void *p2=arena_alloc(&a,4,4); void *p3=arena_alloc(&a,7,8);
    assert(p1&&p2&&p3); assert((uintptr_t)p2%4==0); assert((uintptr_t)p3%8==0);
    size_t used=a.offset; assert(arena_alloc(&a,200,8)==NULL && a.offset==used);
    arena_reset(&a); assert(a.offset==0); void *again=arena_alloc(&a,1,1); assert(again==p1);
    assert(arena_alloc(&a,1,3)==NULL);
    arena_destroy(&a); return 0;
}

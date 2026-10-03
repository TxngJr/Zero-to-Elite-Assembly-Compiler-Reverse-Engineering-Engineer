#include "dynamic_array.h"
#include <assert.h>
int main(void){
    IntVector v; iv_init(&v);
    for(int i=0;i<100;++i) assert(iv_push(&v,i*2));
    assert(v.length==100 && v.capacity>=100);
    int x=-1; assert(iv_get(&v,42,&x) && x==84); assert(!iv_get(&v,100,&x));
    assert(iv_set(&v,0,99)); assert(iv_get(&v,0,&x)&&x==99);
    assert(iv_resize(&v,105,-7)); assert(iv_get(&v,104,&x)&&x==-7);
    assert(iv_resize(&v,3,0) && v.length==3);
    iv_destroy(&v); assert(v.data==0&&v.length==0&&v.capacity==0);
    return 0;
}

#include "dynamic_array.h"
#include <stdint.h>
#include <stdlib.h>
void iv_init(IntVector *v){v->data=NULL;v->length=0;v->capacity=0;}
void iv_destroy(IntVector *v){free(v->data);iv_init(v);}
int iv_reserve(IntVector *v, size_t capacity) {
    if (capacity <= v->capacity) return 1;
    if (capacity > SIZE_MAX / sizeof *v->data) return 0;
    void *tmp = realloc(v->data, capacity * sizeof *v->data);
    if (!tmp) return 0;
    v->data = tmp; v->capacity = capacity; return 1;
}
int iv_push(IntVector *v, int value) {
    if (v->length == v->capacity) {
        size_t next = v->capacity == 0 ? 4 : v->capacity * 2;
        if (next < v->capacity || !iv_reserve(v,next)) return 0;
    }
    v->data[v->length++] = value; return 1;
}
int iv_get(const IntVector *v,size_t index,int *out){if(index>=v->length||!out)return 0;*out=v->data[index];return 1;}
int iv_set(IntVector *v,size_t index,int value){if(index>=v->length)return 0;v->data[index]=value;return 1;}
int iv_resize(IntVector *v,size_t length,int fill){
    if(length>v->capacity && !iv_reserve(v,length)) return 0;
    for(size_t i=v->length;i<length;++i) v->data[i]=fill;
    v->length=length; return 1;
}

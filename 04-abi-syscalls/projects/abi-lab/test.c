#include <assert.h>
#include <stddef.h>
#include <stdio.h>
long long dot_i64(const long long*,const long long*,size_t);
long call_twice(long (*fn)(long), long);
static long square(long x){return x*x;}
int main(void){long long a[]={1,2,3};long long b[]={4,5,6};assert(dot_i64(a,b,3)==32);assert(call_twice(square,5)==50);puts("abi-lab: OK");return 0;}

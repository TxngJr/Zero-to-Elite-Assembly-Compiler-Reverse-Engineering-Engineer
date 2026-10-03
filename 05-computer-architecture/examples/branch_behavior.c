#include <stdint.h>
#include <stdio.h>
static uint64_t count_if(const int *a,size_t n,int threshold){uint64_t count=0;for(size_t i=0;i<n;++i)if(a[i]>threshold)++count;return count;}
int main(void){int predictable[32];int alternating[32];for(int i=0;i<32;++i){predictable[i]=i;alternating[i]=(i&1)?100:-100;}printf("predictable=%llu alternating=%llu\n",(unsigned long long)count_if(predictable,32,15),(unsigned long long)count_if(alternating,32,0));return 0;}

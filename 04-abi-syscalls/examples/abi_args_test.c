#include <assert.h>
#include <stdio.h>
long long sum_six(long long,long long,long long,long long,long long,long long);
long long sum_eight(long long,long long,long long,long long,long long,long long,long long,long long);
int main(void){assert(sum_six(1,2,3,4,5,6)==21);assert(sum_eight(1,2,3,4,5,6,7,8)==36);puts("abi args: OK");return 0;}

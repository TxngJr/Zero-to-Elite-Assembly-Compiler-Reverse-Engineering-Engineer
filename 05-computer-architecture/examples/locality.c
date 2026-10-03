#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 1024
static uint32_t *matrix;
static double seconds(void){return (double)clock()/CLOCKS_PER_SEC;}
int main(void){
    matrix=calloc((size_t)N*N,sizeof *matrix); if(!matrix)return 1;
    volatile uint64_t sum=0; double t0=seconds();
    for(size_t r=0;r<N;++r)for(size_t c=0;c<N;++c)sum+=matrix[r*(size_t)N+c];
    double row=seconds()-t0; t0=seconds();
    for(size_t c=0;c<N;++c)for(size_t r=0;r<N;++r)sum+=matrix[r*(size_t)N+c];
    double col=seconds()-t0;
    printf("row-major %.6f s, column-major %.6f s, checksum=%llu\n",row,col,(unsigned long long)sum);
    free(matrix);return 0;
}

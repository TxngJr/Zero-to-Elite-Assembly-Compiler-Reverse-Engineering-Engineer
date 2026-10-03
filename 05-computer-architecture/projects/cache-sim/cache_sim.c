#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct { uint64_t tag; int valid; } Line;
int main(int argc,char **argv){
    if(argc!=3){fprintf(stderr,"usage: %s LINES BLOCK_BYTES\n",argv[0]);return 2;}
    char *e1,*e2;errno=0;unsigned long lines_ul=strtoul(argv[1],&e1,0),block_ul=strtoul(argv[2],&e2,0);
    if(errno||*e1||*e2||lines_ul==0||block_ul==0){fputs("invalid configuration\n",stderr);return 2;}
    size_t lines=(size_t)lines_ul;uint64_t block=(uint64_t)block_ul;Line *cache=calloc(lines,sizeof *cache);if(!cache)return 1;
    uint64_t addr,hits=0,misses=0;while(scanf("%" SCNx64,&addr)==1){uint64_t block_no=addr/block;size_t index=(size_t)(block_no%lines);uint64_t tag=block_no/lines;if(cache[index].valid&&cache[index].tag==tag)++hits;else{++misses;cache[index].valid=1;cache[index].tag=tag;}}
    printf("hits=%" PRIu64 " misses=%" PRIu64 "\n",hits,misses);free(cache);return 0;
}

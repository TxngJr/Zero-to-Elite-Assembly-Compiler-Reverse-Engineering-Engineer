#include <ctype.h>
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
static void binary(uint64_t value,unsigned width){for(unsigned i=width;i>0;--i)putchar((value>>(i-1))&1u?'1':'0');}
static unsigned useful_width(uint64_t v){if(v<=UINT8_MAX)return 8;if(v<=UINT16_MAX)return 16;if(v<=UINT32_MAX)return 32;return 64;}
int main(int argc,char **argv){
    if(argc!=2){fprintf(stderr,"usage: %s INTEGER\n",argv[0]);return 2;}
    errno=0; char *end=NULL; unsigned long long parsed=strtoull(argv[1],&end,0);
    if(errno||end==argv[1]||*end){fputs("invalid integer\n",stderr);return 2;}
    uint64_t v=(uint64_t)parsed; unsigned width=useful_width(v);
    printf("Decimal : %" PRIu64 "\nHex     : 0x%0*" PRIX64 "\nBinary  : ",v,(int)(width/4),v);
    binary(v,width); putchar('\n');
    if(v<=127u&&isprint((unsigned char)v))printf("ASCII   : %c\n",(int)v);else puts("ASCII   : (not printable ASCII)");
    printf("Width   : %u bits\n",width); return 0;
}

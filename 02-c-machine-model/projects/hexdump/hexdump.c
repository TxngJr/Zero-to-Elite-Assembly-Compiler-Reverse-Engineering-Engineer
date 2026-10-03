#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
static void print_line(const unsigned char *buf,size_t n,size_t offset) {
    printf("%08zx  ",offset);
    for(size_t i=0;i<16;++i){if(i<n)printf("%02x ",buf[i]);else fputs("   ",stdout);if(i==7)putchar(' ');}
    fputs(" |",stdout);
    for(size_t i=0;i<n;++i)putchar(isprint(buf[i])?(int)buf[i]:'.');
    for(size_t i=n;i<16;++i)putchar(' ');
    puts("|");
}
int main(int argc,char **argv){
    if(argc!=2){fprintf(stderr,"usage: %s FILE\n",argv[0]);return 2;}
    FILE *f=fopen(argv[1],"rb"); if(!f){fprintf(stderr,"%s: %s\n",argv[1],strerror(errno));return 1;}
    unsigned char buf[16]; size_t offset=0;
    for(;;){size_t n=fread(buf,1,sizeof buf,f);if(n)print_line(buf,n,offset);offset+=n;if(n<sizeof buf){if(ferror(f)){fputs("read error\n",stderr);fclose(f);return 1;}break;}}
    printf("%08zx\n",offset); fclose(f); return 0;
}

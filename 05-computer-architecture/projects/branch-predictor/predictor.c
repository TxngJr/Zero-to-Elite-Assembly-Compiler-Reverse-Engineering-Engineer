#include <stdio.h>
#include <string.h>
static unsigned update2(unsigned s,int taken){if(taken)return s<3?s+1:s;return s>0?s-1:s;}
int main(int argc,char **argv){const char *seq=argc==2?argv[1]:"TTTNTNTNNNT";unsigned state=1,correct=0,total=0;for(size_t i=0;i<strlen(seq);++i){int actual=seq[i]=='T';if(seq[i]!='T'&&seq[i]!='N'){fputs("sequence must use T/N\n",stderr);return 2;}int pred=state>=2;correct+=(unsigned)(pred==actual);state=update2(state,actual);++total;}printf("correct=%u total=%u final_state=%u\n",correct,total,state);return 0;}

#include <stdio.h>
int main(void) {
    int values[4] = {10,20,30,40};
#ifdef FIXED
    for (size_t i=0;i<4;++i) printf("%d\n",values[i]);
#else
    /* Intentionally buggy training example: run only under sanitizer lab. */
    for (size_t i=0;i<=4;++i) printf("%d\n",values[i]);
#endif
    return 0;
}

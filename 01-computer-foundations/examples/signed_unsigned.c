#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
int main(void) {
    const uint8_t values[] = {0x00u,0x01u,0x7Fu,0x80u,0xFBu,0xFFu};
    for (size_t i=0;i<sizeof values/sizeof values[0];++i) {
        uint8_t u=values[i]; int8_t s=(int8_t)u;
        printf("bits=0x%02" PRIX8 " unsigned=%" PRIu8 " signed=%" PRId8 "\n",u,u,s);
    }
    return 0;
}

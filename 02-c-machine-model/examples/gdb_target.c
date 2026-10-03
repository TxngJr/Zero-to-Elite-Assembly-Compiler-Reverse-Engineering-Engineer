#include <stdint.h>
#include <stdio.h>
struct packet { uint8_t kind; uint32_t id; uint16_t flags; };
static void inspect_me(struct packet *p) {
    p->flags ^= 1u;
    printf("kind=%u id=%u flags=%u\n", (unsigned)p->kind, (unsigned)p->id, (unsigned)p->flags);
}
int main(void){struct packet p={7u,0x11223344u,0x10u};inspect_me(&p);return 0;}

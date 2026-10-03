#include <stdio.h>
typedef struct {
    int values[5];
    int count;
    int total;
} State;

static int add_value(State *s, int value) {
    if (s->count >= 5) return 0;
    s->values[s->count++] = value;
    s->total += value;
    return 1;
}
static int compute_total(void) {
    State s = {{0}, 0, 0};
    for (int i = 0; i < 5; ++i) {
        if (!add_value(&s, (i + 1) * 10)) return -1;
    }
    return s.total;
}
int main(void) {
    int total = compute_total();
    printf("total=%d\n", total);
    return total == 150 ? 0 : 1;
}

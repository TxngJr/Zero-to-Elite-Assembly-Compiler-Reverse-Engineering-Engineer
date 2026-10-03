#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

#define CAPACITY 8

typedef struct {
    unsigned char data[CAPACITY];
    size_t head;
    size_t tail;
    size_t count;
} Pipe;

static size_t pipe_write(Pipe *p, const unsigned char *src, size_t n) {
    size_t written = 0;
    while (written < n && p->count < CAPACITY) {
        p->data[p->tail] = src[written++];
        p->tail = (p->tail + 1) % CAPACITY;
        ++p->count;
    }
    return written;
}

static size_t pipe_read(Pipe *p, unsigned char *dst, size_t n) {
    size_t read = 0;
    while (read < n && p->count != 0) {
        dst[read++] = p->data[p->head];
        p->head = (p->head + 1) % CAPACITY;
        --p->count;
    }
    return read;
}

int main(void) {
    Pipe p = {{0}, 0, 0, 0};
    const unsigned char message[] = "abcdefghi";
    unsigned char out[16] = {0};

    assert(pipe_write(&p, message, 9) == 8);
    assert(p.count == 8);
    assert(pipe_read(&p, out, 3) == 3);
    assert(memcmp(out, "abc", 3) == 0);
    assert(pipe_write(&p, (const unsigned char *)"XYZ", 3) == 3);
    assert(pipe_read(&p, out, 8) == 8);
    assert(memcmp(out, "defghXYZ", 8) == 0);
    assert(p.count == 0);

    puts("ipc-sim: OK");
    return 0;
}

#include <assert.h>
#include <pthread.h>
#include <stdio.h>

enum { THREADS = 4, ITERATIONS = 10000 };

static long counter;
#ifndef INJECT_RACE
static pthread_mutex_t counter_lock = PTHREAD_MUTEX_INITIALIZER;
#endif

static void *worker(void *unused) {
    (void)unused;

    for (int i = 0; i < ITERATIONS; ++i) {
#ifdef INJECT_RACE
        ++counter;
#else
        pthread_mutex_lock(&counter_lock);
        ++counter;
        pthread_mutex_unlock(&counter_lock);
#endif
    }

    return NULL;
}

int main(void) {
    pthread_t threads[THREADS];

    for (int i = 0; i < THREADS; ++i) {
        assert(pthread_create(&threads[i], NULL, worker, NULL) == 0);
    }
    for (int i = 0; i < THREADS; ++i) {
        assert(pthread_join(threads[i], NULL) == 0);
    }

#ifndef INJECT_RACE
    assert(counter == (long)THREADS * ITERATIONS);
#endif

    printf("counter=%ld\n", counter);
    puts("race-lab: OK");
    return 0;
}

#include <assert.h>
#include <stdio.h>

typedef enum {
    TASK_READY,
    TASK_RUNNING,
    TASK_DONE
} TaskState;

typedef struct {
    int pid;
    int remaining;
    TaskState state;
} Task;

static int unfinished(const Task *tasks, int count) {
    for (int i = 0; i < count; ++i) {
        if (tasks[i].state != TASK_DONE) return 1;
    }
    return 0;
}

int main(void) {
    Task tasks[] = {
        {1, 5, TASK_READY},
        {2, 3, TASK_READY},
        {3, 4, TASK_READY},
    };
    const int count = (int)(sizeof tasks / sizeof tasks[0]);
    const int quantum = 2;
    int cursor = 0;
    int ticks = 0;
    int completed = 0;

    while (unfinished(tasks, count)) {
        Task *task = &tasks[cursor];
        cursor = (cursor + 1) % count;

        if (task->state == TASK_DONE) continue;

        task->state = TASK_RUNNING;
        int slice = task->remaining < quantum ? task->remaining : quantum;

        printf("pid=%d run=%d\n", task->pid, slice);
        task->remaining -= slice;
        ticks += slice;

        if (task->remaining == 0) {
            task->state = TASK_DONE;
            ++completed;
        } else {
            task->state = TASK_READY;
        }
    }

    assert(completed == 3);
    assert(ticks == 12);
    printf("completed=%d ticks=%d\n", completed, ticks);
    return 0;
}

CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test clean
all: scheduler-sim
scheduler-sim: scheduler.c
	$(CC) $(CFLAGS) $< -o $@
test: scheduler-sim
	./scheduler-sim > out.txt
	grep -q 'completed=3 ticks=12' out.txt
clean:
	rm -f scheduler-sim out.txt

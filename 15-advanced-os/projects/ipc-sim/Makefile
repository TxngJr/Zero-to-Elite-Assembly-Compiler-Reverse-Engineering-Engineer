CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test clean
all: ipc-sim
ipc-sim: pipe_sim.c
	$(CC) $(CFLAGS) $< -o $@
test: ipc-sim
	./ipc-sim | grep -q 'ipc-sim: OK'
clean:
	rm -f ipc-sim

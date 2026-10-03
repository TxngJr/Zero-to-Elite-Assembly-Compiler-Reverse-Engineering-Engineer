CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test clean
all: vfs-sim
vfs-sim: vfs.c
	$(CC) $(CFLAGS) $< -o $@
test: vfs-sim
	./vfs-sim > out.txt
	grep -q 'vfs-sim: OK' out.txt
clean:
	rm -f vfs-sim out.txt

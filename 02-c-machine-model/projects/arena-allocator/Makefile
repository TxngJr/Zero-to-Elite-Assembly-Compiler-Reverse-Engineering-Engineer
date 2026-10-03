CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all debug sanitize test clean
all: test-arena
test-arena: arena.c test.c arena.h
	$(CC) $(CFLAGS) arena.c test.c -o $@
debug: CFLAGS += -O0
debug: clean all
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
test: test-arena
	./test-arena
clean:
	rm -f test-arena

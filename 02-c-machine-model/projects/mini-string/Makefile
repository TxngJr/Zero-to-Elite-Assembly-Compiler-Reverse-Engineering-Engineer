CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all debug sanitize test clean
all: test-mini-string
test-mini-string: mini_string.c test.c mini_string.h
	$(CC) $(CFLAGS) mini_string.c test.c -o $@
debug: CFLAGS += -O0
debug: clean all
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
test: test-mini-string
	./test-mini-string
clean:
	rm -f test-mini-string

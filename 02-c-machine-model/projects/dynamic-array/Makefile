CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all debug sanitize test clean
all: test-dynamic-array
test-dynamic-array: dynamic_array.c test.c dynamic_array.h
	$(CC) $(CFLAGS) dynamic_array.c test.c -o $@
debug: CFLAGS += -O0
debug: clean all
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
test: test-dynamic-array
	./test-dynamic-array
clean:
	rm -f test-dynamic-array

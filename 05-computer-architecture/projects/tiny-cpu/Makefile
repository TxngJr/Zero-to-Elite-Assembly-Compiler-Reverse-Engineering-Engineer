CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test sanitize clean
all: tiny-cpu
tiny-cpu: tiny_cpu.c
	$(CC) $(CFLAGS) $< -o $@
test: tiny-cpu
	./tiny-cpu | grep -q 'mem\[5\]=30'
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
clean:
	rm -f tiny-cpu

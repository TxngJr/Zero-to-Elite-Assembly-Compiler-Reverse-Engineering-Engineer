CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all debug sanitize test clean
all: zs-hexdump
zs-hexdump: hexdump.c
	$(CC) $(CFLAGS) $< -o $@
debug: CFLAGS += -O0
debug: clean all
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
test: zs-hexdump
	./test.sh
clean:
	rm -f zs-hexdump sample.bin empty.bin out.txt

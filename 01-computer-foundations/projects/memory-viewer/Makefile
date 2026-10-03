CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all debug sanitize test clean
all: memory-viewer
memory-viewer: main.c
	$(CC) $(CFLAGS) $< -o $@
debug: CFLAGS += -O0
debug: clean all
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean all
test: memory-viewer
	./memory-viewer | grep -q 'uint32_t'
	./memory-viewer | grep -q 'virtual addresses'
clean:
	rm -f memory-viewer

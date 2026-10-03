CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all debug sanitize test clean
all: binary-playground
binary-playground: main.c
	$(CC) $(CFLAGS) $< -o $@
debug: CFLAGS += -O0
debug: clean all
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean all
test: binary-playground
	./binary-playground 65 | grep -q 'Hex     : 0x41'
	./binary-playground 255 | grep -q 'Binary  : 11111111'
clean:
	rm -f binary-playground

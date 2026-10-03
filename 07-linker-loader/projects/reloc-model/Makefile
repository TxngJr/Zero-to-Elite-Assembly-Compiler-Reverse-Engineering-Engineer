CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test sanitize clean
all: reloc-model
reloc-model: reloc_model.c
	$(CC) $(CFLAGS) $< -o $@
test: reloc-model
	./reloc-model | grep -q 'ABS64=0x401008'
	./reloc-model | grep -q 'PC32=3836'
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
clean:
	rm -f reloc-model

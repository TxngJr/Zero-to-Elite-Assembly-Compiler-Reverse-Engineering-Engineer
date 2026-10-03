CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test sanitize clean
all: elf-inspector fixture
elf-inspector: elf_inspector.c
	$(CC) $(CFLAGS) $< -o $@
fixture: test_fixture.c
	$(CC) $(CFLAGS) $< -o $@
test: all
	./test.sh
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
clean:
	rm -f elf-inspector fixture out.txt bad.bin

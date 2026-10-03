CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test clean
all: integer-lab
integer-lab: integer_lab.c
	$(CC) $(CFLAGS) $< -o $@
test: integer-lab
	./integer-lab | grep -q 'integer-lab: OK'
clean:
	rm -f integer-lab

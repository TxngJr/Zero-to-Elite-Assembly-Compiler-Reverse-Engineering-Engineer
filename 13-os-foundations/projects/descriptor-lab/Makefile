CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test clean
all: descriptor-lab
descriptor-lab: descriptor_lab.c
	$(CC) $(CFLAGS) $< -o $@
test: descriptor-lab
	./descriptor-lab | grep -q 'idt_gate=16'
clean:
	rm -f descriptor-lab

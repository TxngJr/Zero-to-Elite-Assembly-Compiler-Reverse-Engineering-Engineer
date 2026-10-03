CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test clean inspect
all: abi-lab
abi-lab: abi_lab.s test.c
	$(CC) $(CFLAGS) abi_lab.s test.c -o $@
test: abi-lab
	./abi-lab
inspect: abi-lab
	objdump -d -Mintel abi-lab | sed -n '/<call_twice>/,/^$$/p'
clean:
	rm -f abi-lab

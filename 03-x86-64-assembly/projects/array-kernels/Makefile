CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test clean inspect
all: test-array-kernels
test-array-kernels: kernels.s test.c
	$(CC) $(CFLAGS) kernels.s test.c -o $@
test: test-array-kernels
	./test-array-kernels
inspect: test-array-kernels
	objdump -d -Mintel ./test-array-kernels | sed -n '/<asm_sum_i64>/,/^$$/p'
clean:
	rm -f test-array-kernels *.o

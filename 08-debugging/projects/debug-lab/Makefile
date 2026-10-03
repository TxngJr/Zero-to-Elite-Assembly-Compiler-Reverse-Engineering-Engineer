CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g -fno-omit-frame-pointer
.PHONY: all test gdb-test buggy sanitize-buggy sanitize clean
all: test-fixed
test-fixed: inventory.c test.c inventory.h
	$(CC) $(CFLAGS) inventory.c test.c -o $@
buggy: inventory.c bug_driver.c inventory.h
	$(CC) $(CFLAGS) -DINJECT_BUG inventory.c bug_driver.c -o $@
test: test-fixed
	./test-fixed
gdb-test: test-fixed
	gdb -q -batch -x inspect.gdb ./test-fixed > gdb.out
	grep -q BREAKPOINT_HIT gdb.out
sanitize-buggy: inventory.c bug_driver.c inventory.h
	$(CC) $(CFLAGS) -O1 -DINJECT_BUG -fsanitize=address,undefined -fno-omit-frame-pointer inventory.c bug_driver.c -o $@
sanitize: clean test
clean:
	rm -f test-fixed buggy sanitize-buggy gdb.out

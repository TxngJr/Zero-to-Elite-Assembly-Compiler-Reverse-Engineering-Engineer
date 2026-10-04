CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Wformat=2 -Wformat-security -g

.PHONY: all test unsafe-check clean

all: format-lab

format-lab: format_lab.c
	$(CC) $(CFLAGS) $< -o $@

test: format-lab
	./format-lab > out.txt
	grep -q 'format-lab: OK' out.txt

unsafe-check:
	@set +e; 	$(CC) $(CFLAGS) -Werror=format-security -DINJECT_FORMAT_BUG format_lab.c -o format-unsafe 2>unsafe.err; 	s=$$?; set -e; 	test $$s -ne 0; 	grep -Eq 'format|security' unsafe.err
	@echo '[OK] compiler rejected course-injected non-literal format'

clean:
	rm -f format-lab format-unsafe out.txt unsafe.err

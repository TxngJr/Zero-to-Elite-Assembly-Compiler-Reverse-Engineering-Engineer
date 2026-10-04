CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
SANFLAGS := -O1 -fsanitize=address,undefined -fno-omit-frame-pointer

.PHONY: all test sanitize-demo clean

all: lifetime-lab

lifetime-lab: lifetime_lab.c
	$(CC) $(CFLAGS) $< -o $@

test: lifetime-lab
	./lifetime-lab | grep -q 'lifetime-lab: OK'

sanitize-demo:
	$(CC) $(CFLAGS) $(SANFLAGS) -DINJECT_UAF lifetime_lab.c -o lifetime-uaf-san
	@set +e; ./lifetime-uaf-san >uaf.out 2>uaf.err; s=$$?; set -e; 	test $$s -ne 0; 	grep -Eq 'AddressSanitizer|heap-use-after-free' uaf.err
	@echo '[OK] ASan detected course-injected use-after-free'

clean:
	rm -f lifetime-lab lifetime-uaf-san uaf.out uaf.err

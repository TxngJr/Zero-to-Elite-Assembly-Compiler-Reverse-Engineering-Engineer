CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
SANFLAGS := -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
.PHONY: all test sanitize clean
all: fuzz-lab
fuzz-lab: fuzz_driver.c ../parser-lab/parser.c ../parser-lab/parser.h
	$(CC) $(CFLAGS) -I../parser-lab fuzz_driver.c ../parser-lab/parser.c -o $@
test: fuzz-lab
	./fuzz-lab | grep -q '5000 deterministic cases OK'
sanitize:
	$(CC) $(CFLAGS) $(SANFLAGS) -I../parser-lab fuzz_driver.c ../parser-lab/parser.c -o fuzz-lab-san
	./fuzz-lab-san
clean:
	rm -f fuzz-lab fuzz-lab-san

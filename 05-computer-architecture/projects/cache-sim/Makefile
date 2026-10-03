CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test sanitize clean
all: cache-sim
cache-sim: cache_sim.c
	$(CC) $(CFLAGS) $< -o $@
test: cache-sim
	./test.sh
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
clean:
	rm -f cache-sim out.txt

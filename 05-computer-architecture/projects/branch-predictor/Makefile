CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
.PHONY: all test sanitize clean
all: branch-predictor
branch-predictor: predictor.c
	$(CC) $(CFLAGS) $< -o $@
test: branch-predictor
	./branch-predictor TTTT | grep -q 'total=4'
	./branch-predictor TNTN | grep -q 'total=4'
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean test
clean:
	rm -f branch-predictor

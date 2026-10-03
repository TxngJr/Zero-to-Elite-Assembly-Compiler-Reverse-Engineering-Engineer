CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -g
BUILD := build

.PHONY: all debug test clean
all: $(BUILD)/hello $(BUILD)/streams $(BUILD)/debug_me

debug: CFLAGS += -O0
debug: all

$(BUILD):
	mkdir -p $@

$(BUILD)/hello: examples/hello.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/streams: examples/streams.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/debug_me: examples/debug_me.c | $(BUILD)
	$(CC) $(CFLAGS) -O0 $< -o $@

test:
	CC=$(CC) ./tests/test.sh

clean:
	rm -rf $(BUILD) labs/work-* labs/out.txt labs/err.txt

CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
BUILD := build
SOURCES := $(wildcard examples/*.c)
BINS := $(patsubst examples/%.c,$(BUILD)/%,$(SOURCES))
.PHONY: all debug sanitize test clean
all: $(BINS)
$(BUILD):
	mkdir -p $@
$(BUILD)/%: examples/%.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@
debug: CFLAGS += -O0
debug: clean all
sanitize: CFLAGS += -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
sanitize: clean all
test:
	CC=$(CC) ./tests/test.sh
clean:
	rm -rf $(BUILD)
	$(MAKE) -C projects/binary-playground clean
	$(MAKE) -C projects/memory-viewer clean

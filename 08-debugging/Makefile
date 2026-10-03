CC ?= gcc
BUILD := build
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g -fno-omit-frame-pointer
SOURCES := $(wildcard examples/*.c)
BINS := $(patsubst examples/%.c,$(BUILD)/%,$(SOURCES))
.PHONY: all test sanitize inspect clean
all: $(BINS)
$(BUILD):
	mkdir -p $@
$(BUILD)/%: examples/%.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@
test:
	CC=$(CC) ./tests/test.sh
sanitize:
	$(MAKE) -C projects/debug-lab sanitize CC=$(CC)
	$(MAKE) -C projects/debug-lab sanitize-buggy CC=$(CC)
	@echo "Run ./projects/debug-lab/sanitize-buggy manually to observe ASan report."
inspect: all
	gdb -q -batch -x tests/inspect.gdb $(BUILD)/debug_target
clean:
	rm -rf $(BUILD)
	$(MAKE) -C projects/debug-lab clean

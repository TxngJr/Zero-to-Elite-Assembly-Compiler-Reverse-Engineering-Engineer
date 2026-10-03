CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
BUILD := build
SOURCES := $(filter-out examples/buggy_bounds.c,$(wildcard examples/*.c))
BINS := $(patsubst examples/%.c,$(BUILD)/%,$(SOURCES))
PROJECTS := mini-string dynamic-array arena-allocator hexdump
.PHONY: all debug sanitize test clean projects
all: $(BINS) projects
$(BUILD):
	mkdir -p $@
$(BUILD)/%: examples/%.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@
projects:
	@for p in $(PROJECTS); do $(MAKE) -C projects/$$p all || exit 1; done
debug: CFLAGS += -O0
debug: clean all
sanitize:
	@for p in $(PROJECTS); do $(MAKE) -C projects/$$p sanitize || exit 1; done
	mkdir -p $(BUILD)
	$(CC) $(CFLAGS) -O1 -fsanitize=address,undefined -fno-omit-frame-pointer -DFIXED examples/buggy_bounds.c -o $(BUILD)/bounds-fixed-san
	./$(BUILD)/bounds-fixed-san >/dev/null
test:
	CC=$(CC) ./tests/test.sh
clean:
	rm -rf $(BUILD)
	@for p in $(PROJECTS); do $(MAKE) -C projects/$$p clean; done

CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
BUILD := build
SOURCES := $(wildcard examples/*.c)
BINS := $(patsubst examples/%.c,$(BUILD)/%,$(SOURCES))
PROJECTS := tiny-cpu cache-sim branch-predictor
.PHONY: all test sanitize clean
all: $(BINS)
	@for p in $(PROJECTS); do $(MAKE) -C projects/$$p all || exit 1; done
$(BUILD):
	mkdir -p $@
$(BUILD)/%: examples/%.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@
test:
	CC=$(CC) ./tests/test.sh
sanitize:
	@for p in $(PROJECTS); do $(MAKE) -C projects/$$p sanitize || exit 1; done
clean:
	rm -rf $(BUILD)
	@for p in $(PROJECTS); do $(MAKE) -C projects/$$p clean; done

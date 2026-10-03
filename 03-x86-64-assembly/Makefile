CC ?= gcc
BUILD := build
ASM := $(wildcard examples/*.s)
BINS := $(patsubst examples/%.s,$(BUILD)/%,$(ASM))
.PHONY: all test clean inspect
all: $(BINS)
$(BUILD):
	mkdir -p $@
$(BUILD)/%: examples/%.s | $(BUILD)
	$(CC) -g -no-pie $< -o $@
test:
	CC=$(CC) ./tests/test.sh
inspect: all
	@for b in $(BINS); do echo "=== $$b ==="; objdump -d -Mintel $$b | head -80; done
clean:
	rm -rf $(BUILD)
	$(MAKE) -C projects/array-kernels clean

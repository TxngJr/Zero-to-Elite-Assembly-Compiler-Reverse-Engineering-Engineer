CC ?= gcc
ROOT := ../..
BUILD := $(ROOT)/build/challenges
CFLAGS := -std=c17 -Wall -Wextra -Wpedantic
.PHONY: all clean
all: $(BUILD)/control-o0 $(BUILD)/control-o2 $(BUILD)/control-pie $(BUILD)/control-stripped $(BUILD)/records-o2 $(BUILD)/recursive-o0

$(BUILD):
	mkdir -p $@

$(BUILD)/control-o0: $(ROOT)/examples/control.c | $(BUILD)
	$(CC) $(CFLAGS) -O0 -g -fno-omit-frame-pointer -no-pie $< -o $@

$(BUILD)/control-o2: $(ROOT)/examples/control.c | $(BUILD)
	$(CC) $(CFLAGS) -O2 -g -no-pie $< -o $@

$(BUILD)/control-pie: $(ROOT)/examples/control.c | $(BUILD)
	$(CC) $(CFLAGS) -O2 -g $< -o $@

$(BUILD)/control-stripped: $(BUILD)/control-o2
	cp $< $@
	strip --strip-all $@

$(BUILD)/records-o2: $(ROOT)/examples/records.c | $(BUILD)
	$(CC) $(CFLAGS) -O2 -g -fno-inline -no-pie $< -o $@

$(BUILD)/recursive-o0: $(ROOT)/examples/recursive.c | $(BUILD)
	$(CC) $(CFLAGS) -O0 -g -fno-omit-frame-pointer -no-pie $< -o $@

clean:
	rm -rf $(ROOT)/build/challenges

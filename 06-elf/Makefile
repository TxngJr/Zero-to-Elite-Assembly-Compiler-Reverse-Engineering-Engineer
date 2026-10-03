CC ?= gcc
BUILD := build
.PHONY: all test sanitize inspect clean
all:
	mkdir -p $(BUILD)
	$(CC) -std=c17 -Wall -Wextra -Wpedantic -g examples/hello.c -o $(BUILD)/hello
	$(CC) -std=c17 -Wall -Wextra -Wpedantic -g examples/sections.c -o $(BUILD)/sections
	$(MAKE) -C projects/elf-inspector all CC=$(CC)
test:
	CC=$(CC) ./tests/test.sh
sanitize:
	$(MAKE) -C projects/elf-inspector sanitize CC=$(CC)
inspect: all
	readelf -h $(BUILD)/hello
	readelf -lW $(BUILD)/hello
	readelf -SW $(BUILD)/hello
	readelf -sW $(BUILD)/hello | head -80
clean:
	rm -rf $(BUILD)
	$(MAKE) -C projects/elf-inspector clean

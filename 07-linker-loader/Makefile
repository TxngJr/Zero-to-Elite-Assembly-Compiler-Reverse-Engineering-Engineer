CC ?= gcc
.PHONY: all test sanitize inspect clean
all:
	$(MAKE) -C projects/static-demo all CC=$(CC)
	$(MAKE) -C projects/shared-demo all CC=$(CC)
	$(MAKE) -C projects/reloc-model all CC=$(CC)
test:
	CC=$(CC) ./tests/test.sh
sanitize:
	$(MAKE) -C projects/reloc-model sanitize CC=$(CC)
inspect: all
	$(MAKE) -C projects/static-demo inspect
	$(MAKE) -C projects/shared-demo inspect
clean:
	rm -rf build
	$(MAKE) -C projects/static-demo clean
	$(MAKE) -C projects/shared-demo clean
	$(MAKE) -C projects/reloc-model clean

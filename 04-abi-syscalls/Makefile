CC ?= gcc
.PHONY: all test clean inspect
all:
	$(MAKE) -C projects/abi-lab all
	$(MAKE) -C projects/syscall-cat all
test:
	CC=$(CC) ./tests/test.sh
inspect: all
	$(MAKE) -C projects/abi-lab inspect
	$(MAKE) -C projects/syscall-cat inspect
clean:
	rm -rf build
	$(MAKE) -C projects/abi-lab clean
	$(MAKE) -C projects/syscall-cat clean

PYTHON ?= python3
CC ?= gcc
.PHONY: all test clean
all:
	$(PYTHON) -m py_compile projects/page-walk-sim/page_walk.py
	$(MAKE) -C projects/descriptor-lab all CC=$(CC)
test:
	PYTHON=$(PYTHON) CC=$(CC) ./tests/test.sh
clean:
	rm -rf projects/page-walk-sim/__pycache__
	rm -f split.out demo.out
	$(MAKE) -C projects/descriptor-lab clean

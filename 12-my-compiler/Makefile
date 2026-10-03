PYTHON ?= python3
CC ?= gcc
.PHONY: all test inspect clean

all:
	mkdir -p build
	$(PYTHON) projects/elitec/elitec.py --cc $(CC) examples/factorial.el -o build/factorial

test:
	PYTHON=$(PYTHON) CC=$(CC) ./tests/test.sh

inspect: all
	$(PYTHON) projects/elitec/elitec.py --emit ir examples/factorial.el
	$(PYTHON) projects/elitec/elitec.py --emit asm examples/factorial.el > build/factorial.s
	objdump -d -Mintel build/factorial | sed -n '/<fact>/,/^$$/p'

clean:
	rm -rf build projects/elitec/__pycache__

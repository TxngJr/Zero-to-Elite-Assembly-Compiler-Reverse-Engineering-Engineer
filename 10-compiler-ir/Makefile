PYTHON ?= python3
.PHONY: all test clean
all:
	$(PYTHON) -m py_compile projects/elite-ir/elite_ir.py
test:
	PYTHON=$(PYTHON) ./tests/test.sh
clean:
	rm -rf projects/elite-ir/__pycache__ ir.txt

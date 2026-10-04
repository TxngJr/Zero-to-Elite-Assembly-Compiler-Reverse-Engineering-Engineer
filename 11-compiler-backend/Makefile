PYTHON ?= python3
CC ?= gcc
.PHONY: all test inspect clean
all:
	$(PYTHON) -m py_compile projects/linear-scan/linear_scan.py
	$(PYTHON) projects/elite-backend/elite_backend.py examples/complex.el -o build.s
test:
	PYTHON=$(PYTHON) CC=$(CC) ./tests/test.sh
inspect:
	mkdir -p build
	$(PYTHON) projects/elite-backend/elite_backend.py examples/complex.el -o build/complex.s
	$(CC) build/complex.s -o build/complex
	objdump -d -Mintel build/complex | sed -n '/<fact>/,/^$$/p'
clean:
	rm -rf build build.s projects/elite-backend/__pycache__ projects/linear-scan/__pycache__ tests/__pycache__

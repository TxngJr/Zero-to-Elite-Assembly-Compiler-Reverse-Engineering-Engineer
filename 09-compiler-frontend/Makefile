PYTHON ?= python3
.PHONY: all test clean
all:
	$(PYTHON) -m py_compile projects/elite-frontend/elite_frontend.py
test:
	PYTHON=$(PYTHON) ./tests/test.sh
clean:
	rm -rf projects/elite-frontend/__pycache__

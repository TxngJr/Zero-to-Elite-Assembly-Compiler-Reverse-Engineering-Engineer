CC ?= gcc
PYTHON ?= python3

.PHONY: all build-challenges test clean

all: build-challenges

build-challenges:
	$(MAKE) -C projects/challenge-suite all CC=$(CC)

test:
	CC=$(CC) PYTHON=$(PYTHON) ./tests/test.sh

clean:
	$(MAKE) -C projects/challenge-suite clean
	rm -rf build 		projects/binary-report/__pycache__ 		projects/cfg-extract/__pycache__ 		tests/__pycache__

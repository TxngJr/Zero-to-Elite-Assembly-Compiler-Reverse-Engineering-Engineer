CC ?= gcc
PYTHON ?= python3
.PHONY: all test sanitize fuzz sanitizer-demo clean
all:
	$(MAKE) -C projects/parser-lab all CC=$(CC)
	$(MAKE) -C projects/integer-lab all CC=$(CC)
	$(MAKE) -C projects/fuzz-lab all CC=$(CC)
test:
	CC=$(CC) PYTHON=$(PYTHON) ./tests/test.sh
sanitize:
	$(MAKE) -C projects/parser-lab sanitize CC=$(CC)
	$(MAKE) -C projects/fuzz-lab sanitize CC=$(CC)
fuzz:
	$(MAKE) -C projects/fuzz-lab sanitize CC=$(CC)
sanitizer-demo:
	$(MAKE) -C projects/parser-lab sanitizer-demo CC=$(CC)
clean:
	$(MAKE) -C projects/parser-lab clean
	$(MAKE) -C projects/integer-lab clean
	$(MAKE) -C projects/fuzz-lab clean
	rm -rf projects/crash-triage/__pycache__ triage.out

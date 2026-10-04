CC ?= gcc
PYTHON ?= python3
CLANG ?= clang

.PHONY: all test sanitize fuzz sanitizer-demo advanced-sanitizers clean

all:
	$(MAKE) -C projects/parser-lab all CC=$(CC)
	$(MAKE) -C projects/integer-lab all CC=$(CC)
	$(MAKE) -C projects/fuzz-lab all CC=$(CC)
	$(MAKE) -C projects/lifetime-lab all CC=$(CC)
	$(MAKE) -C projects/format-lab all CC=$(CC)
	$(MAKE) -C projects/race-lab all CC=$(CC)

test:
	CC=$(CC) PYTHON=$(PYTHON) ./tests/test.sh

sanitize:
	$(MAKE) -C projects/parser-lab sanitize CC=$(CC)
	$(MAKE) -C projects/fuzz-lab sanitize CC=$(CC)

fuzz:
	$(MAKE) -C projects/fuzz-lab libfuzzer CLANG=$(CLANG)

sanitizer-demo:
	$(MAKE) -C projects/parser-lab sanitizer-demo CC=$(CC)
	$(MAKE) -C projects/lifetime-lab sanitize-demo CC=$(CC)

advanced-sanitizers:
	$(MAKE) -C projects/race-lab tsan-demo CC=$(CC)

clean:
	$(MAKE) -C projects/parser-lab clean
	$(MAKE) -C projects/integer-lab clean
	$(MAKE) -C projects/fuzz-lab clean
	$(MAKE) -C projects/lifetime-lab clean
	$(MAKE) -C projects/format-lab clean
	$(MAKE) -C projects/race-lab clean
	rm -rf projects/crash-triage/__pycache__ triage.out

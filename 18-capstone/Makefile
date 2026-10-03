PYTHON ?= python3
CC ?= gcc

.PHONY: all audit test inspect clean

all: audit

audit:
	mkdir -p build
	$(PYTHON) projects/final-audit/final_audit.py $(CC)

test:
	PYTHON=$(PYTHON) CC=$(CC) ./tests/test.sh

inspect: test
	@echo '=== Audit summary ==='
	cat build/audit-summary.json
	@echo '=== Artifact manifest ==='
	cat build/manifest.json

clean:
	rm -rf build projects/final-audit/__pycache__

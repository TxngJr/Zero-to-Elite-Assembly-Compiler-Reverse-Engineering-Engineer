CC ?= gcc
PYTHON ?= python3
.PHONY: all test clean
all:
	$(MAKE) -C projects/scheduler-sim all CC=$(CC)
	$(MAKE) -C projects/vfs-sim all CC=$(CC)
	$(MAKE) -C projects/ipc-sim all CC=$(CC)
	$(PYTHON) -m py_compile projects/vm-cow-sim/vm_cow.py
test:
	CC=$(CC) PYTHON=$(PYTHON) ./tests/test.sh
clean:
	$(MAKE) -C projects/scheduler-sim clean
	$(MAKE) -C projects/vfs-sim clean
	$(MAKE) -C projects/ipc-sim clean
	rm -rf projects/vm-cow-sim/__pycache__ vm.out

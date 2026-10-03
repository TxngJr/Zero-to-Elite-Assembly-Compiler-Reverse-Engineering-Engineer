CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -g
.PHONY: all test inspect clean
all: app
calc.o: calc.c calc.h
	$(CC) $(CFLAGS) -fPIC -c calc.c -o $@
libcalc.so: calc.o
	$(CC) -shared -Wl,-soname,libcalc.so -o $@ $<
app: app.c calc.h libcalc.so
	$(CC) $(CFLAGS) app.c -L. -lcalc -Wl,-rpath,'$$ORIGIN' -o $@
test: app
	test "$$(./app)" = '42 42'
inspect: app
	readelf -d app | grep -E 'NEEDED|RUNPATH|RPATH'
	readelf -sW libcalc.so | grep calc_
	objdump -d -Mintel app | grep -E 'calc_(add|mul)' || true
clean:
	rm -f *.o *.so app

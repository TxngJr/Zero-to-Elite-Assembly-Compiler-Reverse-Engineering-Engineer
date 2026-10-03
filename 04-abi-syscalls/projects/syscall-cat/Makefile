CC ?= gcc
.PHONY: all test clean inspect
all: syscall-cat
syscall-cat: cat.s
	$(CC) -nostdlib -static -Wl,--build-id=none cat.s -o $@
test: syscall-cat
	printf 'alpha\nbeta\n' > input.txt
	./syscall-cat input.txt > output.txt
	cmp input.txt output.txt
	@set +e; ./syscall-cat >/dev/null 2>&1; s=$$?; set -e; test $$s -eq 2
	rm -f input.txt output.txt
inspect: syscall-cat
	objdump -d -Mintel syscall-cat | head -160
clean:
	rm -f syscall-cat input.txt output.txt

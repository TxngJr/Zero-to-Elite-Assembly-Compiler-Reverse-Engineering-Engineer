CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
SANFLAGS := -O1 -fsanitize=address,undefined -fno-omit-frame-pointer
.PHONY: all test sanitize sanitizer-demo clean
all: parser-test
parser-test: parser.c test.c parser.h
	$(CC) $(CFLAGS) parser.c test.c -o $@
test: parser-test
	./parser-test | grep -q 'parser-lab: OK'
sanitize:
	$(CC) $(CFLAGS) $(SANFLAGS) parser.c test.c -o parser-test-san
	./parser-test-san
sanitizer-demo:
	$(CC) $(CFLAGS) $(SANFLAGS) -DINJECT_BUG parser.c sanitizer_demo.c -o parser-buggy-san
	@echo 'Built parser-buggy-san. Running it should produce a sanitizer report for the course-injected defect.'
	@set +e; ./parser-buggy-san; s=$$?; set -e; test $$s -ne 0
clean:
	rm -f parser-test parser-test-san parser-buggy-san

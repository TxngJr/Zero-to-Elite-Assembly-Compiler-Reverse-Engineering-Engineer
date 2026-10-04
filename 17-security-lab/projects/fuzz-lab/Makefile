CC ?= gcc
CLANG ?= clang
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g
SANFLAGS := -O1 -fsanitize=address,undefined -fno-omit-frame-pointer

.PHONY: all test sanitize libfuzzer clean

all: fuzz-lab

fuzz-lab: fuzz_driver.c ../parser-lab/parser.c ../parser-lab/parser.h
	$(CC) $(CFLAGS) -I../parser-lab fuzz_driver.c ../parser-lab/parser.c -o $@

test: fuzz-lab
	./fuzz-lab | grep -q '5000 deterministic cases OK'

sanitize:
	$(CC) $(CFLAGS) $(SANFLAGS) -I../parser-lab fuzz_driver.c ../parser-lab/parser.c -o fuzz-lab-san
	./fuzz-lab-san

libfuzzer:
	@command -v $(CLANG) >/dev/null || { echo 'clang is required for libFuzzer target'; exit 2; }
	mkdir -p corpus artifacts
	printf '\x00\x00' > corpus/empty-payload
	printf '\x01\x07\x07' > corpus/one-byte-valid
	$(CLANG) $(CFLAGS) -O1 -fsanitize=fuzzer,address,undefined \
		-I../parser-lab libfuzzer_target.c ../parser-lab/parser.c -o parser-fuzzer
	./parser-fuzzer corpus -artifact_prefix=artifacts/ -runs=2000

clean:
	rm -rf fuzz-lab fuzz-lab-san parser-fuzzer corpus artifacts

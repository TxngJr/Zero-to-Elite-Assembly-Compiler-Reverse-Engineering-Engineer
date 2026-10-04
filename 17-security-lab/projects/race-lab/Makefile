CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g -pthread

.PHONY: all test tsan-demo clean

all: race-lab

race-lab: race_lab.c
	$(CC) $(CFLAGS) $< -o $@

test: race-lab
	./race-lab > out.txt
	grep -q 'counter=40000' out.txt
	grep -q 'race-lab: OK' out.txt

tsan-demo:
	$(CC) $(CFLAGS) -O1 -fsanitize=thread -DINJECT_RACE race_lab.c -o race-tsan
	@set +e; TSAN_OPTIONS=halt_on_error=1 ./race-tsan >tsan.out 2>tsan.err; s=$$?; set -e; 	test $$s -ne 0; 	grep -Eq 'ThreadSanitizer|data race' tsan.err
	@echo '[OK] TSan detected course-injected data race'

clean:
	rm -f race-lab race-tsan out.txt tsan.out tsan.err

CC ?= gcc
AR ?= ar
CFLAGS ?= -std=c17 -Wall -Wextra -Wpedantic -g
.PHONY: all test inspect clean
all: app
triple.o: triple.c util.h
	$(CC) $(CFLAGS) -c triple.c -o $@
square.o: square.c util.h
	$(CC) $(CFLAGS) -c square.c -o $@
libutil.a: triple.o square.o
	$(AR) rcs $@ $^
app.o: app.c util.h
	$(CC) $(CFLAGS) -c app.c -o $@
app: app.o libutil.a
	$(CC) app.o -L. -lutil -Wl,-Map=link.map -o $@
test: app
	test "$$(./app)" = '21 49'
inspect: app
	ar t libutil.a
	nm -C app.o libutil.a
	head -80 link.map
clean:
	rm -f *.o *.a app link.map

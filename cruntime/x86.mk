CC=gcc
CFLAGS=-m32 -O2 -g

SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)

LIBPYYRUNTIME = libpyyruntime.a

$(LIBPYYRUNTIME): $(OBJ)
	$(AR) -rcs $@ $^
	mkdir -p ../x86lib
	mv libpyyruntime.a ../x86lib/
	rm -f $(OBJ)

.PHONY: clean
clean:
	rm -f $(OBJ) $(LIBPYYRUNTIME)

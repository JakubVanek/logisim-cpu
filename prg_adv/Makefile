CROSS      = /home/kuba/x-tools/mipsel-logicpu-elf/bin/mipsel-logicpu-elf-
CC         = $(CROSS)gcc
OBJCOPY    = $(CROSS)objcopy
TARGET_ELF = fibo.elf
TARGET_BIN = fibo.bin

CFLAGS  += -g0 -O3 -Wall -fno-lto -march=mips2 -ffreestanding
LDFLAGS += $(CFLAGS) -T program.lds -nostartfiles -nostdlib

SOURCES = $(wildcard *.c)
OBJECTS = $(filter %.o,$(SOURCES:%.c=%.o))

CRTBEGIN_OBJ := $(shell $(CC) $(CFLAGS) -print-file-name=crtbegin.o)
CRTEND_OBJ   := $(shell $(CC) $(CFLAGS) -print-file-name=crtend.o)
CRTI_OBJ     := $(shell $(CC) $(CFLAGS) -print-file-name=crti.o)
CRTN_OBJ     := $(shell $(CC) $(CFLAGS) -print-file-name=crtn.o)

all: $(TARGET_BIN)

%.o: %.c
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

boot.o: boot.S
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

$(TARGET_ELF): boot.o $(OBJECTS)
	$(CC) $(LDFLAGS) boot.o $(CRTI_OBJ) $(CRTBEGIN_OBJ) $(OBJECTS) -lgcc -lc $(CRTEND_OBJ) $(CRTN_OBJ) -o $@

$(TARGET_BIN): $(TARGET_ELF)
	$(OBJCOPY) -O binary $< $@

clean:
	rm -f *.o $(TARGET_EXE)

.PHONY : default clean all

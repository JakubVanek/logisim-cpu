CROSS      = /home/kuba/x-tools/mipsel-logicpu-elf/bin/mipsel-logicpu-elf-
CC         = $(CROSS)gcc
OBJCOPY    = $(CROSS)objcopy
TARGET_ELF = unaligned.elf
TARGET_BIN = unaligned.bin

CFLAGS  += -g0 -O3 -Wall -fno-lto -march=mips1 -ffreestanding
LDFLAGS += $(CFLAGS) -T program.lds -nostartfiles -nodefaultlibs -nostdlib

SOURCES = $(wildcard *.c)
OBJECTS = $(filter %.o,$(SOURCES:%.c=%.o))

all: $(TARGET_BIN)

%.o: %.c
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

boot.o: boot.S
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

$(TARGET_ELF): boot.o $(OBJECTS)
	$(CC) $(LDFLAGS) boot.o $(OBJECTS) -o $@

$(TARGET_BIN): $(TARGET_ELF)
	$(OBJCOPY) -O binary $< $@

clean:
	rm -f *.o $(TARGET_ELF) $(TARGET_BIN)

.PHONY : default clean all

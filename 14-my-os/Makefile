CC ?= gcc
LD ?= ld
BUILD := build

CFLAGS := -std=c17 -O2 -g 	-Wall -Wextra -Wpedantic -Wconversion -Wshadow 	-ffreestanding -fno-stack-protector -fno-pic -fno-pie 	-fno-asynchronous-unwind-tables -fno-unwind-tables 	-m64 -mno-red-zone -mcmodel=kernel 	-mno-sse -mno-sse2 -mno-mmx -mno-80387

C_SOURCES := 	kernel/kernel.c 	kernel/console.c 	kernel/interrupts.c 	kernel/pmm.c 	kernel/heap.c 	kernel/shell.c

ASM_SOURCES := kernel/boot.s kernel/interrupts.s
C_OBJECTS := $(patsubst kernel/%.c,$(BUILD)/%.o,$(C_SOURCES))
ASM_OBJECTS := $(patsubst kernel/%.s,$(BUILD)/%_asm.o,$(ASM_SOURCES))
OBJECTS := $(ASM_OBJECTS) $(C_OBJECTS)

.PHONY: all kernel test iso qemu qemu-test inspect clean

all: kernel

kernel: $(BUILD)/kernel.elf

$(BUILD):
	mkdir -p $@

$(BUILD)/%.o: kernel/%.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/%_asm.o: kernel/%.s | $(BUILD)
	$(CC) -c $< -o $@

$(BUILD)/kernel.elf: $(OBJECTS) kernel/linker.ld
	$(LD) -m elf_x86_64 -nostdlib -z max-page-size=0x1000 		-T kernel/linker.ld $(OBJECTS) -o $@

test:
	CC=$(CC) LD=$(LD) ./tests/test.sh

iso: kernel
	@command -v grub2-mkrescue >/dev/null || { echo 'missing grub2-mkrescue'; exit 2; }
	@command -v xorriso >/dev/null || { echo 'missing xorriso'; exit 2; }
	rm -rf $(BUILD)/iso
	mkdir -p $(BUILD)/iso/boot/grub
	cp $(BUILD)/kernel.elf $(BUILD)/iso/boot/kernel.elf
	cp boot/grub.cfg $(BUILD)/iso/boot/grub/grub.cfg
	grub2-mkrescue -o $(BUILD)/eliteos.iso $(BUILD)/iso >/dev/null

qemu: iso
	qemu-system-x86_64 -m 128M -cdrom $(BUILD)/eliteos.iso 		-serial stdio -display none -no-reboot -no-shutdown

qemu-test:
	./scripts/qemu-test.sh

inspect: kernel
	readelf -h $(BUILD)/kernel.elf
	readelf -lW $(BUILD)/kernel.elf
	readelf -SW $(BUILD)/kernel.elf
	nm -n $(BUILD)/kernel.elf | head -80

clean:
	rm -rf $(BUILD)

# Troubleshooting

## EliteC Python imports fail
Run compiler tools inside the repository layout. Chapters 10–12 intentionally import earlier educational stages by repository-relative paths.

## EliteC source error prints traceback
That is an internal bug. Normal syntax/type failures should be converted to `CompileError` diagnostics without Python traceback.

## EliteC generated program returns a large value but shell shows another status
Unix process exit status is limited. Use small status-based tests or add an output/reference-interpreter path for larger values.

## Chapter 14 kernel does not link
Confirm x86-64 GNU `ld`, freestanding flags, `-fno-pie`, `-mno-red-zone` and that no libc/runtime symbol leaked into objects.

## Multiboot2 header not found
Run:

```bash
python3 14-my-os/tests/check_multiboot.py 14-my-os/build/kernel.elf
readelf -SW 14-my-os/build/kernel.elf
```

The header must remain aligned and within the first 32 KiB of the file.

## Kernel builds but ISO target says grub2-mkrescue missing
Fedora boot-image tools are optional because normal chapter verification does not require a VM. Install the optional GRUB/xorriso packages through the repo installer or DNF.

## grub2-mkrescue fails while creating ISO
Check `xorriso` and GRUB PC modules. Do not modify your machine's installed bootloader configuration; the course only builds an ISO in the project directory.

## QEMU command missing
Install the Fedora x86 system-emulator package. `make qemu-test` deliberately refuses to proceed when required tools are absent.

## QEMU shows no serial output
Check in this order:
1. Multiboot header validator
2. ELF entry and linker VMAs
3. boot assembly/page tables
4. long-mode transition
5. serial initialization

Use `objdump -d` before changing multiple subsystems at once.

## Kernel hangs after enabling interrupts
Inspect IDT gates, PIC mapping/masks, IRQ EOI and ISR stack behavior. Default exception handler intentionally halts instead of returning from unknown exception frames.

## Keyboard supports only some keys
Expected. Chapter 14 implements a small PS/2 set-1 subset with no Shift/Ctrl/extended-key state machine.

## PMM reports zero frames
Inspect Multiboot memory map and reservation boundary. Early PMM only selects usable memory below 4 GiB because boot page tables identity-map that range.

## gcc / clang / gdb / binutils missing
Run `./scripts/install-fedora-tools.sh` and `./scripts/check-environment.sh`.

## GDB/core/perf restrictions
Containers/security policy can restrict ptrace/core/perf. Do not disable security controls at random; use a local environment where debugging your own process is allowed.

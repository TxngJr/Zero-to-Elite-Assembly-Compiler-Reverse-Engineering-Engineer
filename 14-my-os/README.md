# Chapter 14 — My OS: EliteOS64

บทนี้สร้าง **x86-64 freestanding kernelจริง** ชื่อ EliteOS64.

Milestonesที่ implementationนี้ทำจริง:

```text
Multiboot2 header
→ GRUB handoff in 32-bit protected mode
→ early stack
→ 4 GiB identity map with 2 MiB pages
→ PAE + EFER.LME + paging
→ 64-bit long mode
→ GDT
→ serial + VGA console
→ IDT
→ PIC remap
→ PIT timer IRQ
→ PS/2 keyboard IRQ subset
→ Multiboot2 memory-map parser
→ physical frame bump allocator
→ 64 KiB kernel bump heap
→ tiny interactive shell
```

สิ่งที่ intentionallyยังไม่ทำใน Chapter 14:
- user mode / ring 3
- per-process page tables
- scheduler / processes
- kernel syscalls
- filesystem
- SMP/APIC

หัวข้อเหล่านี้ศึกษาเชิง algorithm/designใน [Chapter 15 — Advanced OS](../15-advanced-os/README.md).

## Navigation
- [Objectives](OBJECTIVES.md)
- [Prerequisites](PREREQUISITES.md)
- [Theory](THEORY.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Challenges](CHALLENGES.md)
- [Common mistakes](COMMON_MISTAKES.md)
- [Mastery test](MASTERY_TEST.md)
- [Answers / hints](ANSWERS.md)

**Previous:** [Chapter 13 — OS Foundations](../13-os-foundations/README.md)  
**Next:** [Chapter 15 — Advanced OS](../15-advanced-os/README.md)

## Build kernel

```bash
make clean test
make kernel
```

## Build bootable ISO on Fedora

```bash
make iso
```

## Run in QEMU

```bash
make qemu
```

Serial output is attached to the terminal.

For an automated boot smoke test on a machine with QEMU + GRUB tooling:

```bash
make qemu-test
```

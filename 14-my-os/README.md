# Chapter 14 — My OS: EliteOS64

บทนี้สร้าง **x86-64 freestanding educational kernelจริง** ชื่อ EliteOS64.

## Runtime milestones ที่ implementation ทำจริง

```text
Multiboot2 header
→ GRUB handoff in 32-bit protected mode
→ early stack
→ 4 GiB identity map with 2 MiB pages
→ PAE + EFER.LME + paging
→ 64-bit long mode
→ GDT
→ COM1 serial + VGA output
→ IDT
→ PIC remap
→ PIT timer IRQ
→ PS/2 keyboard IRQ subset
→ Multiboot2 memory-map parser
→ physical-frame bump allocator
→ 64 KiB kernel bump heap
→ shell input from PS/2 OR serial
```

## Debuggability improvements

Common CPU faultsมี diagnostic path:
- #DE divide error
- #UD invalid opcode
- #GP general protection
- #PF page fault

panic outputแสดง vector, error code, RIP และ #PF แสดง CR2 ก่อน halt.

Unknown vectorsที่ยังไม่ได้ normalizeทั้งหมดใช้ default halt; นี่จึงยังไม่ใช่ production exception framework.

## Static test vs runtime test

```bash
make clean test
```

ตรวจ ELF/Multiboot/symbol/instruction contracts แต่ **ไม่ได้พิสูจน์ว่า kernel bootได้**.

Runtime gate:

```bash
make qemu-test
```

ต้องเห็น serial milestonesถึง:

```text
[BOOT] console ok
[BOOT] pmm/heap ok
[BOOT] idt/pic/pit configured
[BOOT] pit irq ok
[BOOT] shell ready (serial + ps2 input)
elite>
```

`pit irq ok` ถูกพิมพ์หลัง timer_ticksเพิ่มจาก IRQ จริงอย่างน้อย 3 ticks.

## Interactive headless shell

```bash
make qemu
```

ใช้ `-serial stdio -display none`; ตอนนี้ terminal inputเข้า COM1 แล้ว feedเข้า shellจริง จึงพิมพ์:

```text
help
ticks
mem
alloc
clear
```

ได้โดยไม่ต้องเปิด graphical PS/2 display.

## Intentionally not implemented here

- ring 3 user mode
- per-process 4 KiB page tables
- process scheduler/context-switch integration
- kernel syscall ABI
- VFS/filesystem
- APIC/SMP

Chapter 15 ใช้ host-side modelsเพื่อเรียน algorithmsเหล่านี้ก่อน integration.

## Navigation

- [Theory](THEORY.md)
- [Worked examples](WORKED_EXAMPLES.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Mastery test](MASTERY_TEST.md)
- [Rubric](RUBRIC.md)

**Previous:** [Chapter 13 — OS Foundations](../13-os-foundations/README.md)  
**Next:** [Chapter 15 — Advanced OS Models](../15-advanced-os/README.md)

## Self-study quality path

1. [Learner Guide](LEARNER_GUIDE.md)
2. [Theory](THEORY.md)
3. [Worked Examples](WORKED_EXAMPLES.md)
4. [Labs](LABS.md)
5. [Exercises](EXERCISES.md)
6. [Mastery Test](MASTERY_TEST.md)
7. [Rubric](RUBRIC.md)
8. [Answers / Hints](ANSWERS.md)

> `make test` ตรวจ known regressions; ไม่ใช่หลักฐาน mastery.


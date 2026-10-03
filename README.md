# Zero to Elite Assembly, Compiler & Reverse Engineering Engineer

หลักสูตร Systems Engineering แบบลงมือทำบน Fedora/x86-64 ตั้งแต่ Linux, C, Assembly, ABI, Architecture, ELF, Linker/Loader, Debugging, Compiler และตอนนี้ไปถึง **freestanding x86-64 kernel**

## Learning loop

```text
Predict → Build → Run → Observe → Inspect → Debug → Modify → Explain
```

## Stack ที่สร้างจริงแล้ว

```text
EliteLang Source
  ↓
Frontend → Typed AST
  ↓
IR / CFG / Analysis
  ↓
x86-64 Backend
  ↓
EliteC Driver
  ↓
ELF User-Space Executable

and

Firmware / GRUB
  ↓
Multiboot2
  ↓
32-bit Early Boot
  ↓
Long Mode + Page Tables + GDT
  ↓
EliteOS64 Kernel
  ↓
IDT / PIC / PIT / Keyboard
  ↓
PMM / Heap / Mini Shell
```

## Implemented Chapters

- [00 — Linux Systems Laboratory](00-linux-lab/README.md)
- [01 — Computer Foundations](01-computer-foundations/README.md)
- [02 — C Machine Model](02-c-machine-model/README.md)
- [03 — x86-64 Assembly](03-x86-64-assembly/README.md)
- [04 — ABI & Linux Syscalls](04-abi-syscalls/README.md)
- [05 — Computer Architecture](05-computer-architecture/README.md)
- [06 — ELF Internals](06-elf/README.md)
- [07 — Linker & Loader](07-linker-loader/README.md)
- [08 — Debugging Engineering](08-debugging/README.md)
- [09 — Compiler Frontend](09-compiler-frontend/README.md)
- [10 — Compiler IR](10-compiler-ir/README.md)
- [11 — Compiler Backend](11-compiler-backend/README.md)
- [12 — My Compiler: EliteC](12-my-compiler/README.md)
- [13 — OS Foundations](13-os-foundations/README.md)
- [14 — My OS: EliteOS64](14-my-os/README.md)

บท 15–18 ยังอยู่ใน [COURSE_MAP.md](COURSE_MAP.md) และยังไม่สร้าง directory.

## EliteC

```text
.el → tokens → AST → type checking → IR → x86-64 assembly → ELF
```

EliteC CLI รองรับ check/intermediate emits/optimization/build/run และ end-to-end testsผ่าน recursion, loops, short-circuit และ >6 arguments.

## EliteOS64

Chapter 14 kernelทำจริง:

- Multiboot2 header
- protected-mode → long-mode transition
- 4 GiB identity mapด้วย 2 MiB pages
- GDT
- serial + VGA text console
- IDT
- legacy PIC remap
- PIT timer
- keyboard IRQ subset
- Multiboot memory-map parser
- physical frame bump allocator
- kernel bump heap
- mini shell

Processes, user mode, scheduler, syscalls, VFS/filesystem และ SMPอยู่ใน Chapter 15 roadmap.

## Verify

```bash
./scripts/install-fedora-tools.sh
./scripts/check-environment.sh
./scripts/verify-chapters.sh
```

Chapter 14 `make test` ตรวจ kernel ELF/Multiboot/image mechanicsโดยไม่ require VM. ถ้ามี GRUB/QEMU tooling:

```bash
make -C 14-my-os iso
make -C 14-my-os qemu-test
```

## Safety

งาน debugging/reverse engineering/vulnerability researchในบทถัดไปใช้เฉพาะ course binaries, open-source software, CTF/training targets หรือ softwareที่มีสิทธิ์วิเคราะห์ และเน้น defensive understanding/root-cause/fixing.

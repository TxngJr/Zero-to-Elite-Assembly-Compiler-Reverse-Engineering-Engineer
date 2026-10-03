# Zero to Elite Assembly, Compiler & Reverse Engineering Engineer

หลักสูตร Systems Engineering แบบลงมือทำบน Fedora/x86-64 ตั้งแต่พื้นฐานคอมพิวเตอร์และ C ไปจนถึง Assembly, ABI, ELF, Compiler, Operating Systems, Reverse Engineering และ Defensive Security Research.

**Chapters 00–18 implemented.**

## Learning loop

```text
Predict → Build → Run → Observe → Inspect → Debug → Modify → Explain
```

## Full Roadmap

```text
00 Linux Lab
→ 01 Computer Foundations
→ 02 C Machine Model
→ 03 x86-64 Assembly
→ 04 ABI & Syscalls
→ 05 Computer Architecture
→ 06 ELF
→ 07 Linker & Loader
→ 08 Debugging
→ 09 Compiler Frontend
→ 10 Compiler IR
→ 11 Compiler Backend
→ 12 EliteC
→ 13 OS Foundations
→ 14 EliteOS64
→ 15 Advanced OS
→ 16 Reverse Engineering
→ 17 Defensive Security Lab
→ 18 Final Capstone
```

## Major artifacts

### EliteC compiler

```text
EliteLang
→ lexer/parser/type checker
→ IR/CFG
→ x86-64 backend
→ GNU assembly
→ ELF executable
```

Supports functions, recursion, `int/bool`, mutable locals, arithmetic, comparisons, short-circuit logic, `if/else`, `while` and >6 integer arguments.

### EliteOS64

Freestanding x86-64 educational kernel:

```text
Multiboot2
→ protected mode
→ page tables
→ long mode
→ GDT
→ serial/VGA
→ IDT
→ PIC/PIT/keyboard
→ physical frame allocator
→ kernel heap
→ shell
```

Chapter 15 extends OS knowledge through deterministic scheduler/COW/VFS/IPC simulators and advanced design topics such as ring3, TSS, syscalls, APIC/SMP and synchronization.

### Binary analysis / defensive security

Authorized/course-owned targets only:

```text
ELF triage
→ disassembly
→ CFG/data-flow
→ GDB evidence
→ reconstruction
→ local sanitizer/fuzz root-cause workflow
→ patch + regression
```

## Chapters

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
- [15 — Advanced OS](15-advanced-os/README.md)
- [16 — Reverse Engineering](16-reverse-engineering/README.md)
- [17 — Defensive Security Lab](17-security-lab/README.md)
- [18 — Final Capstone](18-capstone/README.md)

## Verify entire course

```bash
./scripts/install-fedora-tools.sh
./scripts/check-environment.sh
./scripts/verify-chapters.sh
```

## Final capstone

```bash
make -C 18-capstone clean test
```

The capstone integrates compiler, ELF/RE tooling, EliteOS64 kernel validation, Advanced-OS simulations and defensive regression tests, then produces a SHA-256 artifact manifest and audit summary.

## Scope / honesty

This repository is an educational systems-engineering course, not a claim that the compiler or kernel is production ready.

Chapter 15 explicitly distinguishes host-side algorithm simulations from kernel-integrated features. Reverse engineering/security work is limited to course-owned or explicitly authorized targets and focuses on debugging, compatibility, root-cause analysis, patching and defensive testing.

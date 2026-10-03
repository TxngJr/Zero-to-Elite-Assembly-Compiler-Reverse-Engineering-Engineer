# Zero to Elite Assembly, Compiler & Reverse Engineering Engineer

หลักสูตร Systems Programming บน Fedora/x86-64 ตั้งแต่ Linux, C, Assembly, ABI, Architecture, ELF, Linker/Loader, Debugging และตอนนี้ถึง **Compiler Frontend → IR → x86-64 Backend**

## Learning loop

```text
Predict → Build → Run → Observe → Inspect → Debug → Modify → Explain
```

## Compiler pipeline ที่สร้างจริง

```text
EliteLang source
  ↓
Lexer → Parser → Typed AST
  ↓
IR / Basic Blocks / CFG
  ↓
Dominators / Liveness / Local Optimization / SSA Concepts
  ↓
x86-64 Backend
  ↓
GNU Assembly
  ↓
GCC/Clang assembler + linker
  ↓
ELF executable
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

บท 12–18 ยังอยู่ใน [COURSE_MAP.md](COURSE_MAP.md) และยังไม่สร้าง directory.

## EliteLang snapshot

รองรับ:
- `int`, `bool`
- functions และ recursion
- typed parameters/returns
- local variables + assignment
- arithmetic/comparisons
- `&&` / `||` แบบ short-circuit
- `if/else`, `while`
- calls รวม >6 integer arguments

Backend ปัจจุบันใช้ stack-slot แบบ spill-everything เพื่อให้ correctness/ABI ชัดก่อน register allocation จริง.

## Verify

```bash
./scripts/install-fedora-tools.sh
./scripts/check-environment.sh
./scripts/verify-chapters.sh
```

## Safety

งาน debugging/reverse engineering/vulnerability research ในบทต่อไปใช้เฉพาะ course binaries, open-source software, CTF/training targets หรือ software ที่มีสิทธิ์วิเคราะห์ และเน้น defensive understanding/root-cause/fixing.

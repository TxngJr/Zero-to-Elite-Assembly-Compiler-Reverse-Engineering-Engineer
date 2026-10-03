# Zero to Elite Assembly, Compiler & Reverse Engineering Engineer

หลักสูตร Systems Programming แบบลงมือทำบน Fedora/x86-64 ตั้งแต่ Linux, data representation, C machine model, Assembly, ABI/syscalls, Computer Architecture ไปจนถึง ELF, Linker/Loader และ Debugging ก่อนต่อยอดสู่ Compiler, OS และ Reverse Engineering

> เป้าหมายคือสร้างพื้นฐานที่ลึกพอให้คุณออกแบบ ตรวจสอบ ดีบัก และเรียน systems ขั้นสูงต่อด้วยตนเอง—not เพื่ออ้างว่าจบ repo เดียวแล้วรู้ทุกอย่าง

## วิธีเรียนหลัก

```text
Predict → Build → Run → Observe → Inspect → Debug → Modify → Explain
```

ก่อนรันตัวอย่าง ให้เขียน prediction จากนั้นใช้ compiler, debugger, disassembler, ELF tools และ system interfacesเก็บ evidence แล้วอธิบายด้วยภาษาของตัวเอง

## Mental model ที่กำลังสร้าง

```text
Source
  ↓
Compiler / Assembler
  ↓
ELF Relocatable Objects
  ↓
Linker
  ↓
ELF Executable / Shared Objects
  ↓
Kernel + Dynamic Loader
  ↓
Process / ABI / Syscalls
  ↓
ISA Execution
  ↓
Microarchitecture
```

และใน debugging/reverse direction:

```text
Symptom → Runtime State → Registers/Memory → Disassembly
        → Symbols/ELF → Control Flow → Root Cause
```

## บทที่พร้อมเรียน

- [00 — Linux Systems Laboratory](00-linux-lab/README.md)
- [01 — Computer Foundations](01-computer-foundations/README.md)
- [02 — C Machine Model](02-c-machine-model/README.md)
- [03 — x86-64 Assembly](03-x86-64-assembly/README.md)
- [04 — System V AMD64 ABI & Linux Syscalls](04-abi-syscalls/README.md)
- [05 — Computer Architecture](05-computer-architecture/README.md)
- [06 — ELF Internals](06-elf/README.md)
- [07 — Linker & Loader](07-linker-loader/README.md)
- [08 — Debugging Engineering](08-debugging/README.md)

บท 09–18 อยู่ใน [COURSE_MAP.md](COURSE_MAP.md) และยังไม่สร้าง directoryจนกว่าจะถึงรอบถัดไป

## Toolchain

หลักสูตรอ้างอิง Fedora Linux x86-64/AMD64 เป็นหลัก:

- GCC / Clang
- GNU binutils: as, ld, readelf, objdump, nm, ar
- GDB
- strace
- Make
- optional: elfutils, perf, valgrind

```bash
./scripts/install-fedora-tools.sh
./scripts/check-environment.sh
./scripts/verify-chapters.sh
```

## โครงสร้างปัจจุบัน

```text
00-linux-lab/
01-computer-foundations/
02-c-machine-model/
03-x86-64-assembly/
04-abi-syscalls/
05-computer-architecture/
06-elf/
07-linker-loader/
08-debugging/
scripts/
```

ทุก chapter มี Objectives, Theory, Labs, Exercises, Challenges, Common Mistakes, Mastery Test, Answers และ executable examples/projects/testsตามความเหมาะสม

## วิธีผ่าน Mastery Gate

1. อ่าน theoryโดยไม่รีบ copy command
2. เขียน prediction
3. build/run
4. inspect evidence
5. explain mismatch
6. ทำ labs/exercises/challenges
7. run tests
8. อธิบาย mental modelได้โดยไม่ท่อง output

อ่าน [STUDY_GUIDE.md](STUDY_GUIDE.md)

## Safety / Reverse Engineering Scope

งาน debugging/reverse engineering/vulnerability researchใช้เฉพาะ course binaries, open-source software, CTF/training targets หรือ softwareที่มีสิทธิ์วิเคราะห์ เน้น understanding, root-cause analysis, defensive debugging และ fixing ไม่สร้าง workflowสำหรับ credential theft, persistence, destructive payloads หรือ unauthorized access

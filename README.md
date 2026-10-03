# Zero to Elite Assembly, Compiler & Reverse Engineering Engineer

หลักสูตร Systems Engineering แบบลงมือทำบน Fedora/x86-64 ครอบคลุม Linux, C, Assembly, ABI, Architecture, ELF, Linker/Loader, Debugging, Compiler, OS, Reverse Engineering และ Defensive Security Research.

## Learning loop

```text
Predict → Build → Run → Observe → Inspect → Debug → Modify → Explain
```

## End-to-end map

```text
Linux / C / Machine Model
  ↓
x86-64 / ABI / Architecture
  ↓
ELF / Linker / Debugging
  ↓
Compiler Frontend → IR → Backend → EliteC
  ↓
OS Foundations → EliteOS64 → Advanced OS Models
  ↓
Reverse Engineering
  ↓
Defensive Security Lab
  ↓
Final Capstone
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
- [15 — Advanced OS](15-advanced-os/README.md)
- [16 — Reverse Engineering](16-reverse-engineering/README.md)
- [17 — Defensive Security Lab](17-security-lab/README.md)

Chapter 18 Final Capstoneยังไม่ถูกสร้าง.

## Advanced OS

Chapter 15ใช้ executable simulatorsเพื่อพิสูจน์ mechanismsก่อน kernel integration:

- round-robin scheduler
- fork/copy-on-write address spaces
- bounded pipe IPC
- in-memory VFS path lookup

เอกสารเชื่อม conceptsไป TSS/ring3/context switching/syscalls/APIC/SMP โดยระบุชัดว่าไม่ได้อ้างว่าฟีเจอร์เหล่านี้ integrateเข้า EliteOS64 Chapter 14แล้ว.

## Reverse Engineering Scope

Chapter 16ใช้เฉพาะ course-owned binariesหรือ targetsที่ได้รับอนุญาต:

```text
provenance/hash
→ ELF triage
→ symbols/strings
→ disassembly
→ CFG/data-flow
→ GDB observations
→ evidence-backed reconstruction
```

มี O0/O2/PIE/stripped challenge variants, binary-report generator และ CFG edge extractor.

## Defensive Security Scope

Chapter 17จำกัดที่ course codeและ defensive workflow:

```text
reproduce
→ sanitizer evidence
→ root cause
→ patch
→ regression
→ fuzz fixed code
→ report
```

Injected bugถูก compileผ่าน flagเฉพาะสำหรับ local sanitizer lab. Default testsใช้ fixed parser.

## Verify

```bash
./scripts/install-fedora-tools.sh
./scripts/check-environment.sh
./scripts/verify-chapters.sh
```

## Authorization / Safety

Reverse engineeringและ security researchใน repositoryนี้ใช้เฉพาะ:
- code/binariesที่สร้างใน course
- softwareที่คุณเขียนเอง
- open-source / CTF / training targetsที่อนุญาตชัดเจน

เนื้อหาเน้น debugging, compatibility, root-cause analysis, patching, fuzzingและ defensive engineering ไม่ใช่ unauthorized access, credential theft, persistence หรือ deploymentของ malicious payloads.

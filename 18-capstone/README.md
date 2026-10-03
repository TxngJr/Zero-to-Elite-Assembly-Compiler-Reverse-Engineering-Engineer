# Chapter 18 — Final Capstone

นี่คือ final integration chapter ของหลักสูตรทั้งหมด.

เป้าหมายไม่ใช่เพิ่ม topic ใหม่แบบแยกส่วน แต่พิสูจน์ว่าคุณสามารถเชื่อมความรู้ทั้ง stack:

```text
source language
→ compiler frontend / IR / backend
→ x86-64 assembly
→ ELF executable
→ linker / loader / ABI
→ debugging / inspection
→ kernel image / boot mechanics
→ advanced OS algorithms
→ reverse engineering
→ defensive security verification
```

Capstone ใช้ **artifacts ที่สร้างใน repository นี้เอง** และทำ final audit ที่ reproducible.

## What the automated capstone does

```text
EliteLang capstone.el
   ↓ EliteC
optimized IR + x86-64 assembly + ELF executable
   ↓
runtime verification
   ↓
readelf / objdump
   ↓
binary-report + CFG extraction
   ↓
EliteOS64 kernel build + Multiboot2 validation
   ↓
Advanced OS simulator tests
   ↓
Reverse Engineering course-suite tests
   ↓
Defensive Security regression tests
   ↓
SHA-256 artifact manifest + final report
```

## Run

```bash
make clean test
```

Artifacts are written to:

```text
18-capstone/build/
├── capstone-app
├── capstone.s
├── capstone.ir
├── capstone.elf.txt
├── capstone.dis
├── binary-report.json
├── cfg.txt
├── eliteos64-kernel.elf
├── manifest.json
└── audit-summary.json
```

## Navigation

- [Objectives](OBJECTIVES.md)
- [Prerequisites](PREREQUISITES.md)
- [Theory](THEORY.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Challenges](CHALLENGES.md)
- [Common mistakes](COMMON_MISTAKES.md)
- [Mastery test](MASTERY_TEST.md)
- [Final checklist](FINAL_CHECKLIST.md)
- [Portfolio template](PORTFOLIO_TEMPLATE.md)
- [Final report template](REPORT_TEMPLATE.md)
- [Answers / hints](ANSWERS.md)

**Previous:** [Chapter 17 — Defensive Security Lab](../17-security-lab/README.md)

## Definition of “finished”

Automated tests are necessary but not enough.

To finish the course, you should also be able to explain—without reading commands from the repository—how source becomes machine execution, how an OS establishes its execution environment, how to inspect an unknown authorized ELF binary, and how to investigate/fix a local memory-safety defect with evidence.

# Chapter 12 — My Compiler: EliteC

บทนี้รวม Chapter 09–11 ให้เป็น compiler command เดียวชื่อ **EliteC**:

```text
EliteLang source
  ↓
Lexer / Parser / Type Checker
  ↓
Typed AST
  ↓
IR / CFG / Analysis / Optional Local Optimization
  ↓
x86-64 System V Backend
  ↓
GNU Assembly
  ↓
GCC/Clang assembler + linker
  ↓
ELF executable
```

นี่คือจุดที่เราเปลี่ยนจาก “เรียน compiler เป็นชิ้น ๆ” เป็น **compiler ที่ผู้ใช้เรียกใช้งานได้จริง**

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

**Previous:** [Chapter 11 — Compiler Backend](../11-compiler-backend/README.md)  
**Next:** [Chapter 13 — OS Foundations](../13-os-foundations/README.md)

## Quick start

```bash
make clean test

python3 projects/elitec/elitec.py --check examples/factorial.el
python3 projects/elitec/elitec.py --emit ir examples/factorial.el
python3 projects/elitec/elitec.py --emit asm examples/factorial.el
python3 projects/elitec/elitec.py examples/factorial.el -o build/factorial
./build/factorial
```

EliteC รุ่นนี้ intentionally ใช้ backend แบบ stack-slot/spill-everything จาก Chapter 11 เพื่อให้ correctnessและ ABIเป็นฐานที่ตรวจสอบได้ก่อนเพิ่ม allocator/optimizerขั้นสูง.

# Chapter 11 — Compiler Backend

บทนี้รับ Elite IR แล้ว emit **x86-64 System V AMD64 assembly** ที่ assembler/linker สร้าง ELF executable ได้จริง.

```text
IR/CFG
→ baseline x86-64 instruction selection
→ ABI lowering
→ stack-frame layout
→ GNU assembly
→ ELF
```

## Baseline backend ที่ใช้จริง

Code generator หลัก intentionally ใช้ **spill-everything stack slots** เพื่อให้ reasoning เรื่อง ABI, calls, signed division และ control flow อ่านได้ตรงไปตรงมา.

มัน handle:
- arithmetic/comparisons
- branches/loops
- short-circuit CFG
- calls/recursion
- 0–8+ integer arguments
- signed division/modulo
- 16-byte call-site alignment

## Register-allocation lab

`projects/linear-scan/` เป็น implementation ของ **linear-scan allocation algorithm จริงบน live intervals** พร้อม tests สำหรับ:
- register reuse
- overlapping intervals
- spill under pressure
- invalid/duplicate interval rejection

มันยัง **ไม่ได้ถูก integrate เข้า baseline codegen** เพราะ integrationต้อง model call clobbers, fixed registers, callee-saved state, spill insertion และ SSA/parallel copiesก่อน.

ดังนั้นอย่าอ้างว่า EliteC ใช้ linear-scan allocationใน generated codeจน integrationนั้นเกิดขึ้นจริง.

## Commands

```bash
make clean test
python3 projects/linear-scan/linear_scan.py
make inspect
```

## Navigation

- [Theory](THEORY.md)
- [Worked examples](WORKED_EXAMPLES.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Mastery test](MASTERY_TEST.md)
- [Rubric](RUBRIC.md)

**Previous:** [Chapter 10 — Compiler IR](../10-compiler-ir/README.md)  
**Next:** [Chapter 12 — My Compiler](../12-my-compiler/README.md)

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


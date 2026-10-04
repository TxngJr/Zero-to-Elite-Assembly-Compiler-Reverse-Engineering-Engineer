# Chapter 16 — Reverse Engineering

บทนี้ฝึก reverse engineering แบบมีสิทธิ์และควบคุมได้กับ **course-owned / explicitly authorized binaries**.

```text
provenance + SHA-256
→ ELF metadata
→ symbols / strings / relocations
→ disassembly
→ functions
→ basic blocks / CFG
→ data-flow / structures
→ GDB observation
→ evidence-backed reconstruction
```

## Challenge variants

- O0
- O2
- PIE
- stripped
- struct/record access
- recursion

## Tooling ที่ทำจริง

### binary-report

Required ELF tools (`file/readelf`) fail → report failจริง. Optional symbol extractionเช่น `nm` บันทึก status แทนการซ่อน failure.

### cfg-extract

ตอนนี้ไม่ได้เป็นแค่ jump-summary:
- identify direct branch targets
- create basic-block leaders
- add branch edges
- add fallthrough edges
- list direct calls
- JSON mode สำหรับตรวจ structure

ยังไม่ใช่ production recursive disassembler: indirect jumps/calls, exception edges, overlapping code และ advanced recoveryยังเป็น limitations.

## Scope

ใช้กับ:
- binariesจาก course
- softwareที่คุณเขียนเอง
- open-source/training/CTF targetที่อนุญาตชัดเจน

ไม่ใช้เพื่อ unauthorized access, credential theft, persistence หรือ bypass licensing/authentication.

## Commands

```bash
make clean test
make build-challenges
python3 projects/binary-report/binary_report.py build/challenges/control-o2
python3 projects/cfg-extract/cfg_extract.py --json build/challenges/control-o0
```

## Navigation

- [Theory](THEORY.md)
- [Worked examples](WORKED_EXAMPLES.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Mastery test](MASTERY_TEST.md)
- [Rubric](RUBRIC.md)

**Previous:** [Chapter 15](../15-advanced-os/README.md)  
**Next:** [Chapter 17](../17-security-lab/README.md)

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


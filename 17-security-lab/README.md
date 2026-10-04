# Chapter 17 — Defensive Security Lab

บทนี้ฝึก **defensive vulnerability research** บน course-owned code หรือ explicitly authorized targets เท่านั้น.

```text
scope
→ reproduce locally
→ sanitizer/compiler/debugger evidence
→ minimize
→ root cause
→ patch
→ regression
→ fuzz fixed code
→ defensive report
```

## Executable labs

- `parser-lab/` — bounds validation + course-injected OOB for ASan
- `integer-lab/` — checked size arithmetic
- `lifetime-lab/` — correct ownership + course-injected UAF for ASan
- `format-lab/` — safe formatting + `-Wformat-security` rejection demo
- `race-lab/` — mutex-correct counter + optional TSan race demo
- `fuzz-lab/` — deterministic pseudo-random smoke **และ coverage-guided libFuzzer target**
- `crash-triage/` — sanitizer-log summarizer

## Fixed-code gate

```bash
make clean test
```

Default tests run fixed implementations only.

## Diagnostic demonstrations

```bash
make sanitizer-demo
make fuzz
make advanced-sanitizers
```

- `sanitizer-demo` ตั้งใจ compile course-only OOB/UAF variantsและต้องถูก ASanจับ
- `fuzz` ใช้ Clang libFuzzer + ASan/UBSanกับ fixed parser
- `advanced-sanitizers` ใช้ TSanกับ course-injected data raceเมื่อ runtime supportพร้อม

การไม่มี crashไม่ใช่ proof of security.

## Safety boundary

ไม่สอนหรือ require exploit payload, persistence, credential theft, stealth หรือ testing third-party systemsโดยไม่มี authorization.

## Navigation

- [Theory](THEORY.md)
- [Worked examples](WORKED_EXAMPLES.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Mastery test](MASTERY_TEST.md)
- [Rubric](RUBRIC.md)

**Previous:** [Chapter 16](../16-reverse-engineering/README.md)  
**Next:** [Chapter 18](../18-capstone/README.md)

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


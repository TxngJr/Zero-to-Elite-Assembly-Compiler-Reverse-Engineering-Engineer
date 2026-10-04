# Chapter 08 — Debugging Engineering

บทนี้เปลี่ยน GDB จาก “เครื่องมือหยุดโปรแกรม” ให้เป็น workflow เชิงวิศวกรรม:

```text
symptom → reproduce → narrow → observe state → form hypothesis
        → test hypothesis → root cause → fix → regression test
```

เราดีบัก source, assembly, registers, memory, signals, optimized code และ core dumps โดยใช้ course-owned toy programs.

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

**Previous:** [Chapter 07 — Linker & Loader](../07-linker-loader/README.md)  
**Next:** [Chapter 09 — Compiler Frontend](../09-compiler-frontend/README.md)

```bash
make clean test
make sanitize
```
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

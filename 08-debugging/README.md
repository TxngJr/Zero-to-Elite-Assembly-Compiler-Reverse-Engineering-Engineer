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

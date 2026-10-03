# Chapter 08 — Debugging Engineering

บทนี้เปลี่ยน GDB จาก “เครื่องมือหยุดโปรแกรม” ให้เป็น workflow เชิงวิศวกรรม:

```text
symptom → reproduce → narrow → observe state → form hypothesis
        → test hypothesis → root cause → fix → regression test
```

เราดีบักทั้ง source, assembly, registers, memory, signals, optimized code และ core dumps โดยใช้ **course-owned toy programs** เท่านั้น

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
- [Course map](../COURSE_MAP.md)

**Previous:** [Chapter 07 — Linker & Loader](../07-linker-loader/README.md)  
**Next:** Chapter 09 — Compiler Frontend (**not implemented yet**)

```bash
make clean test
make sanitize
```

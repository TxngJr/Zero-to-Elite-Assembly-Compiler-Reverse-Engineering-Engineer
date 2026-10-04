# Chapter 02 — C Machine Model

บทนี้ไม่ใช่คอร์ส C syntax ทั่วไป แต่ใช้ C เป็นสะพานจาก source code ไปสู่ bytes, addresses, object representation, compiler transformations และ machine behavior เพื่อเตรียม Chapter 03 x86-64 Assembly

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

**Previous:** [Chapter 01](../01-computer-foundations/README.md)  
**Next:** Chapter 03 — x86-64 Assembly (**not implemented yet**)

## Build everything

```bash
make test
```

Sanitizer build of projects:

```bash
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

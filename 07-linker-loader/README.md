# Chapter 07 — Linker & Loader

Chapter 06ทำให้เราเห็นโครง ELF; บทนี้อธิบายว่า **ทำไม `.o` หลายไฟล์ถึงกลายเป็น executable/shared library ได้** และหลังจากนั้น kernel + dynamic loader ทำอะไรเพื่อสร้าง process image

```text
symbols → resolution → relocations → archive/shared libraries
        → GOT/PLT → dynamic metadata → loader mappings
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
- [Answers / hints](ANSWERS.md)
- [Course map](../COURSE_MAP.md)

**Previous:** [Chapter 06 — ELF Internals](../06-elf/README.md)  
**Next:** [Chapter 08 — Debugging Engineering](../08-debugging/README.md)

```bash
make clean test
make inspect
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

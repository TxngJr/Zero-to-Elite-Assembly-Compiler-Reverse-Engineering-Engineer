# Chapter 05 — Computer Architecture

บทนี้เชื่อมสิ่งที่เราเขียนใน Assembly เข้ากับสิ่งที่ CPU และ memory hierarchy ต้องทำจริง ตั้งแต่ datapath/control, pipeline, hazards, branch prediction, caches, virtual memory, TLB, multicore และ performance reasoning

เราแยก **ISA** ออกจาก **microarchitecture** อย่างชัดเจน: binary เดียวกันอาจรันบน CPU หลายรุ่นที่ implement x86-64 ต่างกันภายใน

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

**Previous:** [Chapter 04](../04-abi-syscalls/README.md)  
**Next:** [Chapter 06 — ELF Internals](../06-elf/README.md)

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

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

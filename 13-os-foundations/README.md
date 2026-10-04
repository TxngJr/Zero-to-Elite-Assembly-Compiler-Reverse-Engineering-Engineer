# Chapter 13 — OS Foundations

บทนี้เปลี่ยนจาก Linux user-space ไปสู่ **freestanding x86-64 kernel engineering**.

ใน user-space เราเคยพึ่ง:

```text
process loader + virtual memory + libc/runtime + kernel syscalls
```

แต่ kernelแรกของเราต้องจัดการเอง:

```text
boot protocol
→ CPU mode
→ descriptor tables
→ page tables
→ interrupts
→ devices
→ memory management
→ kernel runtime
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

**Previous:** [Chapter 12 — My Compiler](../12-my-compiler/README.md)  
**Next:** [Chapter 14 — My OS](../14-my-os/README.md)

## Runnable foundation projects

```bash
make clean test

python3 projects/page-walk-sim/page_walk.py split 0x7fffffffffff
./projects/descriptor-lab/descriptor-lab
```

Chapterนี้ intentionallyจำลอง privileged mechanismsใน user-space projectsก่อนเข้า Chapter 14 ซึ่ง build kernelจริง.
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

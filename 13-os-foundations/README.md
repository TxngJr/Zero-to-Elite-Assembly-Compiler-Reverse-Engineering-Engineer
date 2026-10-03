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

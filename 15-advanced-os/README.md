# Chapter 15 — Advanced OS Models & Integration Design

Chapter 14 มี kernelที่ boot/interrupt/memory/shellได้จริง. บทนี้ศึกษา mechanisms ขั้นต่อไปด้วย **host-side executable models** เพื่อแยก algorithm correctnessออกจาก privileged integration complexity.

```text
TSS / ring 3 design
→ address spaces
→ fork / copy-on-write
→ context switching
→ scheduling
→ syscalls
→ IPC / pipes
→ VFS
→ synchronization
→ APIC / SMP concepts
```

## Executable models

- `scheduler-sim/` — round-robin scheduling
- `vm-cow-sim/` — fork/COW + frame refcounts
- `ipc-sim/` — bounded byte pipe
- `vfs-sim/` — in-memory path lookup

## Important scope boundary

Modelsเหล่านี้ **ไม่ใช่ kernel-integrated features**. Passing Chapter 15 tests does not mean EliteOS64 has:
- user mode
- scheduler
- syscalls
- filesystem
- SMP

การ integrateจริงเป็น capstone/extension workและต้องมี QEMU runtime evidence.

## Commands

```bash
make clean test
```

## Navigation

- [Theory](THEORY.md)
- [Worked examples](WORKED_EXAMPLES.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Mastery test](MASTERY_TEST.md)
- [Rubric](RUBRIC.md)

**Previous:** [Chapter 14 — EliteOS64](../14-my-os/README.md)  
**Next:** [Chapter 16 — Reverse Engineering](../16-reverse-engineering/README.md)

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


# Chapter 15 — Advanced OS

Chapter 14 ทำให้ EliteOS64 boot, รับ interrupts, จัด physical frames และมี kernel shell ได้แล้ว บทนี้ต่อยอดแนวคิดที่ต้องมีเพื่อไปจาก “single-address-space educational kernel” ไปสู่ระบบปฏิบัติการที่มี isolation/processes/files/filesystem abstractions.

หัวข้อหลัก:

```text
robust exceptions
→ TSS / ring 3
→ address spaces
→ fork / copy-on-write
→ process model
→ context switching
→ scheduler
→ syscalls
→ IPC / pipes
→ VFS
→ synchronization
→ SMP / APIC
```

บทนี้ใช้ **host-side executable simulators** เพื่อพิสูจน์ algorithms ก่อนนำไป integrateกับ kernelจริงใน capstone/extension work. จึงไม่อ้างว่า EliteOS64 Chapter 14 มี process isolationหรือ filesystemจริงแล้ว.

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

**Previous:** [Chapter 14 — My OS](../14-my-os/README.md)  
**Next:** [Chapter 16 — Reverse Engineering](../16-reverse-engineering/README.md)

```bash
make clean test
```

Projects:
- `projects/scheduler-sim/` — round-robin process scheduling
- `projects/vm-cow-sim/` — address spaces + fork + copy-on-write
- `projects/vfs-sim/` — in-memory VFS path lookup/read
- `projects/ipc-sim/` — bounded byte-pipe semantics

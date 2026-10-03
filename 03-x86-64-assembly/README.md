# Chapter 03 — x86-64 Assembly

บทนี้เปลี่ยนจากการ “ดู assembly ที่ compiler สร้าง” ไปสู่การเขียนและ reason เกี่ยวกับ x86-64 instructions ด้วยตัวเองบน Linux/Fedora

เราใช้ GNU assembler ผ่าน GCC และเขียน **Intel syntax** ด้วย `.intel_syntax noprefix`. Chapter 04 จะเจาะ System V AMD64 ABI และ Linux syscall แบบเต็ม; บทนี้เน้น instruction semantics, registers, flags, memory addressing และ control flow

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

**Previous:** [Chapter 02 — C Machine Model](../02-c-machine-model/README.md)  
**Next:** [Chapter 04 — ABI & Linux Syscalls](../04-abi-syscalls/README.md)

```bash
make clean test
make inspect
```

> ตัวอย่าง `main` ถูกเรียกผ่าน C runtime เพื่อให้เราโฟกัส instruction semantics ก่อน สัญญาการเรียก function จะอธิบายอย่างเป็นระบบใน Chapter 04

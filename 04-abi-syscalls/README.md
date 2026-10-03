# Chapter 04 — System V AMD64 ABI & Linux Syscalls

บทนี้ตอบคำถามที่ Chapter 03 ตั้งไว้: function หนึ่งรู้ได้อย่างไรว่า argument อยู่ register ไหน, register ไหนต้อง preserve, stack ต้อง align อย่างไร และ user program ขอ kernel ทำงานผ่าน syscall อย่างไร

ใช้ Linux x86-64 + System V AMD64 ABI เป็นเป้าหมายหลัก

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

**Previous:** [Chapter 03](../03-x86-64-assembly/README.md)  
**Next:** [Chapter 05 — Computer Architecture](../05-computer-architecture/README.md)

```bash
make clean test
make inspect
```

Project `syscall-cat` ใช้เฉพาะไฟล์ที่คุณระบุเองใน lab และเป็นตัวอย่างระบบ I/O พื้นฐาน ไม่ใช่เครื่องมือเข้าถึงข้อมูลที่ไม่ได้รับอนุญาต

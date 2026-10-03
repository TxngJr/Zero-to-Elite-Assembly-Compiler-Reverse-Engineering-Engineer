# Chapter 00 — Linux Systems Laboratory

บทนี้สร้าง laboratory บน Fedora ให้พร้อมสำหรับ systems programming และสอน mental model ขั้นต้นของ shell, filesystem, permissions, process, `/proc`, compiler pipeline, Make, Git และ GDB

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

**Previous:** none  
**Next:** [Chapter 01 — Computer Foundations](../01-computer-foundations/README.md)

## Quick start

```bash
../scripts/check-environment.sh
make test
```

ระหว่างเรียนอย่ารัน command ที่ไม่เข้าใจ โดยเฉพาะ `rm`, `chmod`, `kill` และ command ที่มี `sudo`. Labs ในบทนี้ออกแบบให้ทำใน directory ของ repo และ process ที่เราสร้างเอง

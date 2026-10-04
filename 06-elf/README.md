# Chapter 06 — ELF Internals

บทนี้แกะ **ELF (Executable and Linkable Format)** จากไฟล์จริงบน Linux/x86-64 ตั้งแต่ ELF header, program headers, section headers, symbols, relocations ไปจนถึงความต่างระหว่าง “สิ่งที่ linker ใช้” กับ “สิ่งที่ loader ใช้”

เป้าหมายคือมอง binary แล้วตอบได้ว่า file type อะไร, entry point อยู่ไหน, loader map segment ไหน, code/data อยู่ตรงไหน และ symbols/relocations อยู่ตรงไหน

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

**Previous:** [Chapter 05 — Computer Architecture](../05-computer-architecture/README.md)  
**Next:** [Chapter 07 — Linker & Loader](../07-linker-loader/README.md)

```bash
make clean test
make inspect
```

โปรเจกต์หลักคือ `projects/elf-inspector/` ซึ่งอ่าน ELF64 แบบ defensive: validate magic/class/data encoding และตรวจ file bounds ก่อนเดินตาราง headers

> `elf-inspector` รองรับ ELF64 little-endian แบบ header counts ปกติบน target course เท่านั้น; ELF32, big-endian และ extended section/program-header numbering เป็นหัวข้อขยายและจะถูก rejectแทนการเดา format.
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

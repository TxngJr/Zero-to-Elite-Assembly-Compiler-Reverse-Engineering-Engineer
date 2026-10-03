# Chapter 11 — Compiler Backend

บทนี้รับ Elite IR จาก Chapter 10 แล้ว emit **x86-64 System V AMD64 assembly** ที่ GCC/Clang assemble + link เป็น executableจริง

```text
typed AST → IR/CFG → x86-64 codegen → .s → assembler/linker → ELF → run
```

Backend รุ่นนี้ตั้งใจเรียบง่าย: virtual valuesทุกตัวถูก spillลง stack slotsก่อน เพื่อแยก correct code generation ออกจาก register allocation.

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

**Previous:** [Chapter 10 — Compiler IR](../10-compiler-ir/README.md)  
**Next:** [Chapter 12 — My Compiler](../12-my-compiler/README.md)

```bash
make clean test
make inspect
```

Tests compile EliteLang programs to assembly, link them with the selected C compiler driver, execute them, and verify exit status.

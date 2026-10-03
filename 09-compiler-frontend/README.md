# Chapter 09 — Compiler Frontend

บทนี้เริ่มสร้างภาษาเล็กชื่อ **EliteLang** จริง ๆ จาก source text ไปเป็น:

```text
source → tokens → AST → semantic/type checks
```

ภาษาในรอบนี้รองรับ functions, `int`/`bool`, variables, assignment, arithmetic, comparisons, `&&`/`||`, function calls, `if/else`, `while`, และ `return`.

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

**Previous:** [Chapter 08 — Debugging Engineering](../08-debugging/README.md)  
**Next:** [Chapter 10 — Compiler IR](../10-compiler-ir/README.md)

```bash
make clean test
python3 projects/elite-frontend/elite_frontend.py --tokens examples/valid.el
python3 projects/elite-frontend/elite_frontend.py --ast examples/valid.el
```

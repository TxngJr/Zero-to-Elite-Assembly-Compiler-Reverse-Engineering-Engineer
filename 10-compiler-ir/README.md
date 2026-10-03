# Chapter 10 — Compiler Intermediate Representation

Chapter 09 เปลี่ยน source เป็น typed AST; บทนี้ lower AST ไปเป็น **three-address-style IR + basic blocks + CFG** เพื่อให้ optimization และ backend ไม่ต้องทำงานกับ syntax โดยตรง

Pipeline:

```text
typed AST → lowering → basic blocks / CFG
          → dominators / liveness
          → local optimizations
          → SSA concepts / phi placement hints
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

**Previous:** [Chapter 09 — Compiler Frontend](../09-compiler-frontend/README.md)  
**Next:** [Chapter 11 — Compiler Backend](../11-compiler-backend/README.md)

```bash
make clean test
python3 projects/elite-ir/elite_ir.py --ir examples/loop.el
python3 projects/elite-ir/elite_ir.py --live examples/loop.el
```

> SSA ในบทนี้เป็น educational analysis/phi-candidate step ไม่ใช่ production-grade full SSA construction. Full compiler integrationจะต่อใน Chapter 12.

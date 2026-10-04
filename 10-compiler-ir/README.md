# Chapter 10 — Compiler Intermediate Representation

Chapter 09 เปลี่ยน source เป็น typed AST; บทนี้ lower AST ไปเป็น **three-address-style IR + basic blocks + CFG** และทำ data-flow/SSA analysis ที่ executable/testable.

```text
typed AST
→ lowering
→ basic blocks / CFG
→ dominators / liveness
→ local constant optimization
→ immediate dominators / dominance frontiers
→ phi placement
→ SSA renaming
```

## สิ่งที่ทำจริง

- CFG successors/predecessors
- dominator sets
- liveness fixed-point
- signed-i64 constant foldingตาม [language specification](../LANGUAGE_SPEC.md)
- phi-candidate teaching view
- **full educational SSA construction**: immediate dominators, dominance frontiers, phi placement และ dominator-tree renaming

`--ssa` ตอนนี้แสดง SSA ที่ rename source variablesจริง; `--phi-candidates` เก็บ heuristic เดิมไว้เพื่อเปรียบเทียบ.

## สิ่งที่ยังไม่ใช่ production optimizer

- IR ยังไม่ encode rich typesทุก instruction
- SSA formยังไม่ได้ feedเข้า baseline backend
- ยังไม่มี SSA destruction/global value numbering/LICM
- optimizerหลักยังเป็น local constant propagation/folding

## Commands

```bash
make clean test
python3 projects/elite-ir/elite_ir.py --ir examples/loop.el
python3 projects/elite-ir/elite_ir.py --dom examples/diamond.el
python3 projects/elite-ir/elite_ir.py --live examples/loop.el
python3 projects/elite-ir/elite_ir.py --phi-candidates examples/diamond.el
python3 projects/elite-ir/elite_ir.py --ssa examples/diamond.el
```

## Navigation

- [Objectives](OBJECTIVES.md)
- [Theory](THEORY.md)
- [Worked examples](WORKED_EXAMPLES.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Challenges](CHALLENGES.md)
- [Mastery test](MASTERY_TEST.md)
- [Rubric](RUBRIC.md)
- [Answers / hints](ANSWERS.md)

**Previous:** [Chapter 09 — Compiler Frontend](../09-compiler-frontend/README.md)  
**Next:** [Chapter 11 — Compiler Backend](../11-compiler-backend/README.md)

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


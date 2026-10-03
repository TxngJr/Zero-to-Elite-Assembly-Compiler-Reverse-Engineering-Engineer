# Labs

1. Lower arithmetic ASTเป็น tempsด้วยมือ.
2. ดู `--ir examples/loop.el` แล้ววาด CFG.
3. ระบุ predecessors/successorsทุก block.
4. Lower if/elseและหา merge block.
5. Lower whileและหา back edge.
6. Lower `&&` และยืนยัน RHSอยู่คนละ block.
7. Lower `||` และยืนยัน short-circuit.
8. คำนวณ dominator setsของ diamondก่อนเปิด `--dom`.
9. คำนวณ USE/DEFของ loop blocks.
10. ทำ liveness iterationบนกระดาษ.
11. `--live` cross-check.
12. `fold.el` ก่อน/หลัง `--opt`.
13. ระบุ instructionที่ DCEลบได้/ไม่ได้ในตัวอย่างที่มี call.
14. `--ssa diamond.el` หา phi candidate `x`.
15. ออกแบบ full SSA rename stepsเป็น diagram.

# Mastery Test

1. AST→IR lowering
2. basic blocks/terminators
3. CFG
4. if/while lowering
5. short-circuit
6. dominators
7. use/def
8. liveness equations
9. fixed point
10. constants
11. DCE safety
12. SSA/phi
13. loop phi
14. IR verification
15. `--ir` loop outputอธิบายได้
16. `--dom` diamondถูก
17. `--live` loopถูก
18. `--ssa` candidateถูก
19. `--opt` folds 6*7+1→43
20. เพิ่ม IR analysis/passหนึ่งอย่างพร้อม tests

Pass ≥85% + `make test`.
## Scoring — 100 points

ใช้ [RUBRIC.md](RUBRIC.md): Concepts 20, Prediction 10, Lab evidence 20, Implementation 25, Inspection/debugging 15, Explanation/limitations 10. **Pass:** ≥85, Implementation ≥18/25, Lab evidence ≥14/20. `make test` เป็น automated prerequisite เท่านั้น.

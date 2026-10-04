# Mastery Test

1. ISA vs ABI vs API
2. args 1–8 mapping
3. return caveats
4. caller/callee-saved
5. stack alignment
6. frame pointer omission
7. red zone
8. C↔assembly interop
9. indirect call
10. syscall register map
11. RCX/R11 clobber
12. raw error vs errno
13. `_start` argc/argv
14. partial I/O
15. strace/GDB evidence
16. `abi-lab`ผ่าน
17. `syscall-cat`ผ่าน empty/text/large tests
18. debug deliberate callee-saved violation

Pass ≥85% + `make test` ผ่าน + อธิบาย function ABIและ syscall ABIได้โดยไม่เปิดชีท.
## Scoring — 100 points

ใช้ [RUBRIC.md](RUBRIC.md): Concepts 20, Prediction 10, Lab evidence 20, Implementation 25, Inspection/debugging 15, Explanation/limitations 10. **Pass:** ≥85, Implementation ≥18/25, Lab evidence ≥14/20. `make test` เป็น automated prerequisite เท่านั้น.

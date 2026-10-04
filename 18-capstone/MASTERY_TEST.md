# Mastery Test

## Automated Gate

```bash
make clean test
```

Must produce:
- capstone executable
- optimized IR
- generated x86-64 assembly
- ELF inspection
- disassembly
- binary report
- CFG report
- EliteOS64 kernel copy
- SHA-256 manifest
- audit summary

## Oral / Written Defense

Explain without reading source:

1. characters→tokens→AST→IR→assembly→ELF
2. why compiler IR exists
3. SysV first six integer argument registers
4. how argument 7+ are passed
5. caller vs callee saved registers
6. stack alignment before calls
7. sections vs segments
8. PIE vs non-PIE
9. relocation purpose
10. dynamic loader role
11. crash site vs root cause
12. source stepping vs instruction stepping at O2
13. hosted vs freestanding C
14. Multiboot2 role
15. 32-bit→64-bit boot transition
16. CR3 role
17. GDT vs IDT
18. PMM vs VMM vs heap
19. process vs thread
20. COW algorithm
21. scheduler READY/BLOCKED/RUNNING states
22. VFS abstraction
23. static vs dynamic RE
24. fact vs inference
25. ASan/UBSan limits
26. fuzzing limits
27. hardening vs root-cause fix
28. why reproducible hashes matter
29. current EliteC technical debt
30. current EliteOS64 technical debt

## Pass Criteria

- automated test passes
- ≥85% oral/written defense
- final report completed
- portfolio claims are evidence-backed
- limitations documented explicitly
- all RE/security work stays within authorized scope
## Scoring — 100 points

ใช้ [RUBRIC.md](RUBRIC.md): Concepts 20, Prediction 10, Lab evidence 20, Implementation 25, Inspection/debugging 15, Explanation/limitations 10. **Pass:** ≥85, Implementation ≥18/25, Lab evidence ≥14/20. `make test` เป็น automated prerequisite เท่านั้น; ต้องส่ง human capstone deliverables ใน [ASSIGNMENT.md](ASSIGNMENT.md) ด้วย.

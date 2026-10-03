# Labs

1. Run fixed parser tests.
2. Read packet format and list all required bounds checks.
3. Build `make sanitizer-demo`; observe ASan on injected bug locally.
4. Identify first invalid project memory access—not later frames.
5. Compare `parser.c` guarded code paths with `INJECT_BUG`.
6. Explain why claimed length must be checked against both input size and destination capacity.
7. Add boundary tests length=0, max, max+1.
8. Run integer-lab and explain checked multiplication.
9. Add checked addition test near SIZE_MAX.
10. Run fuzz-lab deterministic corpus.
11. Increase iterations locally and record seed.
12. Add a valid seed packet.
13. Modify local parser copy with a harmless logic bug; see regression catch it.
14. Minimize one rejected packet to smallest reproducer.
15. Run crash-triage on sample ASan log.
16. Write root-cause paragraph without exploit speculation.
17. Compare hardening metadata of parser binaries.
18. Compile with stack protector/PIE and explain why source fix still required.
19. Create security report from REPORT_TEMPLATE.
20. Add one regression test for a new parser edge case.

# Mastery Test

1. C pipeline .c→executable
2. identifier/object/type/value/address/storage
3. `sizeof` array vs pointer
4. pointer `p=&x` และ dereference
5. pointer arithmetic/one-past
6. พิสูจน์ array≠pointer
7. C string representation
8. struct padding/alignment ด้วย offsetof
9. stack model caveats
10. malloc/calloc/realloc/free + ownership
11. scope vs storage duration
12. static/extern contexts
13. function pointer/indirect call
14. const declarators
15. volatile limitations
16. UB/implementation-defined/unspecified
17. warnings/ASan/UBSan limits
18. optimization observability
19. ทำนาย struct offsets
20. หา realloc bug
21. หา out-of-bounds loop
22. อ่าน sanitizer report
23. O0/O2 constant folding
24–27. mini-string, dynamic-array, arena, hexdump tests ผ่าน
28. GDB inspect pointer/array/struct สำเร็จ

Pass ≥85% + required projects/tests.
## Scoring — 100 points

ใช้ [RUBRIC.md](RUBRIC.md): Concepts 20, Prediction 10, Lab evidence 20, Implementation 25, Inspection/debugging 15, Explanation/limitations 10. **Pass:** ≥85, Implementation ≥18/25, Lab evidence ≥14/20. `make test` เป็น automated prerequisite เท่านั้น.

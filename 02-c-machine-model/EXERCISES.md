# Exercises

## วิธีทำแบบฝึกหัดชุดนี้

รายการ numbered prompts ด้านล่าง **ไม่ใช่คำศัพท์ให้ท่อง**. ทุกข้อให้ตอบ 4 ส่วน: **Explain** ด้วยภาษาตัวเอง, **Concrete example** จาก artifact ในบท, **Evidence** เป็น command/code/calculation/output, และ **Boundary / misconception** อย่างน้อยหนึ่งข้อ. โจทย์คำนวณ/assembly/CFG ต้องแสดงขั้นตอน; โจทย์ code ต้องมี test/evidence.


## Objects/types
1. แยก name/type/value/address ของ `uint32_t x=7`
2. C รับประกัน `sizeof(char)` เท่าไร
3. ทำไมไม่ hard-code `sizeof(int)==4`
4. `sizeof` คืน type อะไร
5. ทำไม exact address ไม่ควรอยู่ deterministic test

## Pointers/arrays
6. วาด `int x=5; int *p=&x;`
7. `*p=9` เปลี่ยน object ใด
8. `p+1` หมายถึงอะไร
9. one-past pointer ทำอะไรได้/ไม่ได้
10. array decay คืออะไร
11. contexts ที่ array ไม่ decay 2 ตัวอย่าง
12. `sizeof a` vs `sizeof &a`
13. `a+1` vs `&a+1`
14. pointer subtraction/comparison ต้องระวังอะไร
15. integer↔pointer cast ไม่ควรเป็น default techniqueเพราะอะไร

## Strings/structs/unions
16. "ABC" ใช้กี่ char elements
17. `strlen` vs `sizeof`
18. bounded copy ต้องรับ capacity เพราะอะไร
19. struct padding เกิดเพื่ออะไร
20. `offsetof` ช่วยอะไร
21. ทำไม raw struct ไม่ portable format
22. union shared storage คืออะไร
23. วิธี inspect representation ที่ portable กว่า union punning
24. enum ควรถูก serialize โดยสมมติ fixed width หรือไม่

## Lifetime/scope/heap
25. scope vs lifetime
26. automatic object lifetime
27. file-scope vs block-scope `static`
28. `malloc` initialize bytes หรือไม่
29. `calloc` ต่างอย่างไร
30. ทำไม `ptr=realloc(ptr,n)` เสี่ยง leak
31. dangling pointer
32. double free
33. ownership ลดบัคอะไร
34. “stack grows down” เป็น C rule หรือไม่

## Functions/qualifiers/preprocessor
35. declaration vs definition
36. function pointer use case
37. `const int *p` vs `int *const p`
38. const=compile-time constant เสมอหรือไม่
39. volatile thread-safe หรือไม่
40. macro evaluate argument หลายครั้งได้อย่างไร
41. header guard
42. header interface
43. translation unit
44. extern multi-file

## UB/tooling/optimization
45. UB 4 ประเภท
46. implementation-defined vs unspecified
47. warnings prove correctness หรือไม่
48. ASan ตรวจอะไร
49. UBSan ตรวจอะไร
50. optimized out คืออะไร
51. constant folding
52. dead-code elimination
53. source line ไม่ map 1:1 assembly เพราะอะไร
54. GCC/Clang assembly ต่างกันแต่ถูกทั้งคู่ได้หรือไม่
55. debugger observation ทำ UB defined หรือไม่

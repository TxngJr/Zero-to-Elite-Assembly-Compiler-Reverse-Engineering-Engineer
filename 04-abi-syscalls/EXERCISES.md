# Exercises

## วิธีทำแบบฝึกหัดชุดนี้

ทุก numbered prompt ต้องตอบ 4 ส่วน: **Explain**, **Concrete example**, **Evidence**, และ **Boundary / misconception**. โจทย์คำนวณ/assembly/CFG ต้องแสดงขั้นตอน; โจทย์ code ต้องมี test/evidence.


1. ISA/ABI/APIต่างกันอย่างไร
2. integer args 1–6อยู่ไหน
3. arg7/8ที่ entryอยู่ไหน
4. scalar integer returnทั่วไปอยู่ไหน
5. callee-saved GPRs
6. caller-saved GPRs
7. เหตุผลของ save contract
8. alignmentก่อน CALL
9. alignmentที่ entryหลัง CALLโดยทั่วไป
10. pushหนึ่งครั้งกระทบ alignmentอย่างไร
11. frame pointerมีไว้ทำอะไร
12. RBP frameจำเป็นทุก functionไหม
13. red zoneกี่ bytes
14. kernelทำไมไม่พึ่ง user red zone
15. Direction Flag rule
16. variadic caveat
17. linkerตรวจ ABI correctnessทั้งหมดได้ไหม
18. indirect callยังใช้ ABIเดิมไหม
19. syscall number register
20. syscall args registers
21. arg4ทำไม R10
22. syscall clobberอะไร
23. raw error vs libc errno
24. read=0หมายถึงอะไร
25. partial writeคืออะไร
26. robust write loopทำอะไรบ้าง
27. `main` vs `_start`
28. argc initial location
29. argv[1] simplified offset
30. syscall numbers portableไหม
31. `-nostdlib` ตัดอะไร
32. static binaryใน labหมายถึงอะไร
33. straceเป็น evidenceอะไร
34. negative raw errorต้องเช็ค signedเพราะอะไร
35. nested functionใช้ RBXต้องทำอะไร
36. callerต้องเก็บ RAXเดิมข้าม callไหมถ้าต้องใช้
37. leaf functionยังต้อง preserve callee-savedไหม
38. stack restoreทุก pathทำไมสำคัญ
39. CFIเกี่ยวกับ unwindingอย่างไร
40. ABI violationทำไม linkผ่านแต่ runtimeพังได้

# Exercises — Compiler IR / Data Flow / SSA

## Response contract

ทุกข้อให้มี **Explain + Concrete example + Evidence + misconception/boundary**. ข้อ algorithmต้องแสดง intermediate sets/graph ไม่ใช่ตอบผลสุดท้ายอย่างเดียว.

## A. IR / CFG

1. Lower sourceที่มี `if/else` หนึ่งชุดเป็น IRด้วยมือ: ระบุ blocks, instructions, terminators.
2. วาด CFG ของ `examples/diamond.el`; เขียน predecessor/successor setsทุก blockก่อนรัน tool.
3. วาด CFG ของ loopและชี้ back edge.
4. อธิบาย basic block invariant: branch/returnอยู่ตรงไหนและทำไม instructionหลัง terminatorไม่ควร execute.
5. สร้าง malformed IRที่ branchไป blockไม่มีอยู่และเขียน verifier/testให้ reject.

## B. Dominators

6. คำนวณ dominator setsของ diamondด้วย fixed-point iterationทีละรอบ.
7. หา immediate dominatorของทุก block.
8. เพิ่ม blockกลางก่อน joinแล้วคำนวณใหม่.
9. อธิบาย “A precedes B” ไม่เท่ากับ “A dominates B” พร้อม counterexample.
10. คำนวณ dominance frontierของ diamondและอธิบายว่าทำไม joinอยู่ใน frontierของ branch blocks.

## C. Liveness

11. สำหรับ `x=a; y=x+b; return y` คำนวณ USE/DEF/IN/OUTด้วยมือ.
12. สร้าง CFG 2 blocksที่ valueถูก defineใน blockแรกและใช้ใน blockสอง; คำนวณ live-out.
13. เพิ่ม dead temporaryหนึ่งตัวและอธิบายว่าข้อมูล livenessช่วย DCEอย่างไร.
14. อธิบาย use-before-defกับ live-inต่างกันอย่างไร.
15. เขียน unit test exact sets; ห้ามใช้ grepว่า outputมีคำ `out=`.

## D. Constant Folding / i64 Semantics

16. คำนวณ `INT64_MAX / 3` แบบ exactและพิสูจน์ optimizerตรง.
17. คำนวณ `-7 / 3` และ `-7 % 3` ตาม trunc-toward-zero.
18. ทดสอบ `INT64_MAX + 1` wrapping.
19. พิสูจน์ว่า `INT64_MIN / -1` ไม่ถูก foldเพราะต้อง preserve runtime trap.
20. เพิ่ม randomized differential testsอย่างน้อย 100 arithmetic cases: optimized vs unoptimized behavior.

## E. SSA

21. จาก diamondที่ xถูก assignคนละค่าในสอง branch ให้ place phiด้วย dominance frontier.
22. ทำ rename stack/version numbersด้วยมือและเขียน resulting SSA.
23. ทำ loop variable `i` แล้วอธิบาย phi inputจาก entryกับ back edge.
24. ตรวจว่า SSA versionหนึ่งถูก defineครั้งเดียว.
25. อธิบาย `undef`ใน educational SSAหมายถึงอะไรและทำไม production compilerต้องมี stronger rules.
26. เขียน testที่ usesหลัง joinต้องชี้ phi destination version ไม่ใช่ source nameเดิม.
27. อธิบาย SSA destruction: phiต้องกลายเป็น edge copiesอย่างไร และ critical-edge problemคืออะไร.

## F. Optimization Pipeline Design

28. เสนอ pass orderสำหรับ constant fold, CFG simplification, DCE และ SSA construction พร้อมเหตุผล.
29. เขียน IR verifier checklist: unique labels, valid targets, terminator required, definition/use invariants.
30. สร้าง minimal bug reportสำหรับ optimizer mismatch: source, IR before/after, expected, actual, regression test.

## Practical submission

ส่ง graph/sets calculation, SSA derivation, exact semantic unit tests และ optimization differential testอย่างน้อยหนึ่งชุด.

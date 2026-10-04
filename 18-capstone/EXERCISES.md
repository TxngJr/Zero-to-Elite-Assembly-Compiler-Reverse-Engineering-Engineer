# Exercises — Final Capstone

Exercisesนี้ไม่ใช่คำศัพท์ท่องจำ. ทุกข้อให้มี **Explain + Concrete example + Evidence + misconception/boundary** และอ้าง artifact/hash/commandที่เกี่ยวข้อง.

## A. End-to-End Compiler

1. จาก `capstone.el` วาด tokens→AST→IR→assembly→ELF pipelineและระบุ information gained/lostแต่ละ boundary.
2. เลือก function `fact`; ชี้ AST/IR/assembly/disassembly evidenceที่ represent logicเดียวกัน.
3. อธิบาย 8-argument callด้วย ABI evidence.
4. เปรียบ optimized/unoptimized capstoneและยืนยัน behavior equivalence.
5. หา technical debtหนึ่งจุดใน EliteCและเสนอ test-first patch plan.

## B. ELF / Debugging / RE

6. บันทึก SHA-256ของ capstone executableและ kernel; ตรวจ manifest.
7. ระบุ ELF Type/Machine/entry/LOAD segmentsของ capstone app.
8. ทำ blind pseudocode functionหนึ่งก่อนเปิด source.
9. ใช้ CFG extractorระบุ blocks/edges/callsของ functionนั้น.
10. ใช้ GDBยืนยัน static hypothesisหนึ่งข้อ.
11. แยก Facts/Inferences/Unknownsอย่างน้อย 5/5/3รายการ.

## C. OS

12. วาด EliteOS64 boot state transitionsจาก GRUBถึง kernel_main.
13. ใช้ kernel disassemblyพิสูจน์ long-mode setup.
14. รัน QEMU runtime gateและแนบ serial log.
15. พิสูจน์ serial `ticks` commandทำงานจริงจาก qemu test.
16. อธิบาย PMM limitationและสิ่งที่ Chapter15 simulatorยังไม่ได้ integrate.
17. ออกแบบ patchหนึ่งชิ้นตาม Deliverable B พร้อม acceptance tests.

## D. Advanced OS

18. Trace scheduler simหนึ่ง full runและเขียน state transitions.
19. Trace COW fork/writeพร้อม frame refcounts.
20. Trace pipe wrap-around.
21. Trace VFS path lookup.
22. เลือกหนึ่ง modelและเขียน kernel-integration dependency graph.

## E. Defensive Engineering

23. รัน Chapter17 fixed regression suite.
24. รัน injected sanitizer demoและเขียน root-cause summary.
25. รัน libFuzzerเมื่อ availableและบันทึก corpus/run evidence.
26. อธิบาย hardening vs fixด้วย course artifact.
27. เขียน one-page defensive reportที่ impactไม่เกิน evidence.

## F. Learner-created Work

28. ทำ compiler deliverableจาก `ASSIGNMENT.md`; ส่ง design+patch+tests.
29. ทำ OS deliverableและ QEMU evidence.
30. ทำ blind authorized RE deliverable.
31. ทำ defensive bug-fix deliverable.
32. ทำ engineering defense 10 questionsโดยไม่เปิด notes.

## G. Final Reflection

33. ระบุ 5 mental modelsที่เปลี่ยนจากก่อนเรียน.
34. ระบุ 5 limitationsของ repoอย่างซื่อสัตย์.
35. เขียน roadmap 3 เดือนเพื่อเปลี่ยน educational compiler/kernelไปขั้นถัดไป พร้อม milestones/tests.

## Pass

Exercisesเป็น evidenceประกอบ rubric; `make test` อย่างเดียวไม่ถือว่าทำ exercisesหรือจบ capstone.

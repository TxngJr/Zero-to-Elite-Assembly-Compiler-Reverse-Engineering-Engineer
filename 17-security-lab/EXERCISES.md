# Exercises — Defensive Security Lab

Course-owned code only. เป้าหมายคือ detection/root-cause/fix/regression ไม่ใช่ exploitation.

## Response contract

ทุกข้อให้มี **Explain + Concrete example + Evidence + misconception/boundary**.

## A. Bounds / Parser

1. เขียน parser invariantสำหรับ header, claimed length, input remaining, destination capacity.
2. รัน fixed parser testsแล้วเพิ่ม boundary `0`, `PAYLOAD_MAX`, `PAYLOAD_MAX+1`.
3. รัน injected ASan demo; ระบุ error class, access type/size, first project frame.
4. อธิบาย crash site vs root causeใน report.
5. minimize malformed inputให้เล็กที่สุดที่ยัง trigger injected defectใน local lab.
6. patch local intentionally-buggy copyแล้วแสดง regression red→green.

## B. Integer Safety

7. พิสูจน์ checked additionก่อน `a+b` ด้วย `SIZE_MAX`.
8. พิสูจน์ checked multiplicationก่อน `a*b`.
9. สร้าง truncation caseจาก `size_t`ไป `uint16_t`และออกแบบ validationก่อน cast.
10. อธิบาย unsigned wrapที่ definedแต่ยังสร้าง allocation-size logic bugได้.
11. เพิ่ม property-style testsหลายค่าใกล้ boundaries.

## C. Lifetime / Format / Race

12. รัน lifetime fixed testและ injected UAF ASan demo; วาด ownership/alias graph.
13. อธิบายทำไม set pointerหนึ่งตัว NULLไม่แก้ aliasesอื่น.
14. รัน format unsafe-checkและอธิบาย `printf("%s", input)` vs `printf(input)`.
15. รัน race fixed test; ระบุ synchronization invariant.
16. ถ้า environmentรองรับ TSan ให้รัน injected race; ถ้าไม่รองรับให้บันทึก limitationอย่างซื่อสัตย์.
17. เปรียบเทียบ mutexกับ atomicสำหรับ counter use case.
18. อธิบายทำไม `volatile`ไม่แก้ data race.

## D. Fuzzing

19. รัน deterministic 5000-case smokeและบอกว่ามัน **ไม่ใช่ coverage-guided fuzzing**.
20. รัน libFuzzer targetด้วย seed corpus; เก็บ command/output summary.
21. เพิ่ม valid seedหนึ่งตัวที่ครอบ boundary pathใหม่.
22. ถ้าพบ failure: save artifact → minimize → deterministic reproduce → regression.
23. ถ้าไม่พบ failure: อธิบายว่าทำไมยังสรุป “secure”ไม่ได้.
24. ออกแบบ fuzz target APIให้ deterministic/no network/no persistent side effects.

## E. Hardening / Impact

25. ใช้ `readelf`ดู PIE/NX/RELROของ course binaryและอธิบายสิ่งที่แต่ละ mitigationไม่ได้แก้.
26. เปรียบเทียบ buildมี/ไม่มี stack protector; อย่าอ้างว่ามันแก้ root cause.
27. เขียน impact statementของ OOB labโดยระบุ reachability/attacker control/privilege assumptions.
28. เขียนตัวอย่าง impact claimที่เกิน evidenceแล้วแก้ให้ grounded.
29. สร้าง patch review checklist: validation position, types, error path, regression boundaries.

## F. Report / Engineering

30. ใช้ crash-triage scriptกับ sample ASan logและตรวจผลด้วยมือ.
31. สร้าง reportหนึ่งฉบับจาก templateพร้อม scope, reproduction, root cause, fix, regression, fuzz result, residual risk.
32. เพิ่ม defensive labใหม่หนึ่ง bug classแบบ course-ownedที่มี fixed default + injected diagnostic build.
33. เขียน disclosure/authorization paragraphสำหรับ hypothetical third-party researchโดยไม่ให้ exploit details.

## Practical submission

ต้องมี sanitizer evidence, fixed regression, checked arithmetic tests, fuzz evidence, grounded impact statement และ defensive reportหนึ่งฉบับ.

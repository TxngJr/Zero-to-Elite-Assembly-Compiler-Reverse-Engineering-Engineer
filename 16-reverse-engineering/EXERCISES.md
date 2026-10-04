# Exercises — Authorized Reverse Engineering

ใช้เฉพาะ course-owned/explicitly authorized binaries.

## Response contract

ทุกข้อให้ตอบอย่างน้อย 4 ส่วนตามมาตรฐานทั้ง course: **Explain** ด้วยภาษาตัวเอง, **Concrete example** จาก course binary, **Evidence** จาก tool/output และ **misconception / boundary** ที่ต้องระวัง. สำหรับงาน RE ให้แยกในคำตอบเป็น:
- **Fact** — สิ่งที่เห็นตรงจาก artifact/runtime
- **Inference** — สิ่งที่อนุมานจาก fact
- **Evidence** — command/address/block/register/bytes ที่รองรับ
- **Unknown / misconception** — สิ่งที่ยังพิสูจน์ไม่ได้หรือข้อสรุปที่ควรหลีกเลี่ยง

## A. Triage

1. Build challenge suiteแล้วบันทึก SHA-256ของ O0/O2/PIE/stripped variants.
2. ใช้ `file/readelf -h` เปรียบเทียบ PIEกับ non-PIE; อธิบาย ELF Type.
3. เปรียบเทียบ section/program headersและบอกว่าอะไรเป็น loader evidence.
4. เปรียบเทียบ symbol tableก่อน/หลัง strip; ระบุ metadataที่ยังเหลือ.
5. ใช้ `readelf -d`/relocationsระบุ dynamic dependencies/import machinery.

## B. Disassembly / ABI

6. เลือก functionใน unstripped binaryแล้วระบุ args/returnจาก SysV evidence.
7. หา signed vs unsigned comparisonจาก Jccและเขียน pseudocode.
8. หา RIP-relative accessหนึ่งจุดและคำนวณ target addressจาก next RIP + displacement.
9. หา loop induction/stride/accumulatorใน records binary.
10. infer Record field offsetsจาก memory operandsโดยไม่เปิด source; ให้ confidenceแต่ละ field.
11. หา recursive callใน recursive binaryและแยก base case/recursive case.
12. ระบุ compiler/runtime noiseเช่น PLT/startupที่ไม่ใช่ app logic.

## C. CFG

13. รัน cfg extractorกับ control-o0; วาด basic blocksจาก JSON.
14. เลือก conditional blockและยืนยัน branch + fallthrough edges.
15. เลือก unconditional jumpและยืนยันไม่มี implicit fallthrough.
16. แยก call edgeจาก intra-function CFG edge.
17. หา loop back edgeใน binaryที่มี loop.
18. อธิบาย limitationต่อ indirect jumps/jump tablesและเขียน Unknownแทน edgeปลอม.

## D. Dynamic Validation

19. ใช้ GDBหยุด functionหนึ่งตัวใน unstripped course binary; เก็บ RDI/RSI/RAX evidence.
20. ใช้ `x/` inspect array/struct bytesแล้วเทียบ static inference.
21. บน PIE binary ใช้ mappingsหา load baseและแปลง link-time↔runtime addressหนึ่งจุด.
22. เปลี่ยน inputอย่างน้อย 3 ค่าเพื่อยืนยัน branch hypothesisหลาย path.
23. เขียน claimหนึ่งข้อที่ dynamic runเดียว **ไม่** สามารถพิสูจน์.

## E. O0/O2 / Stripped

24. เปรียบเทียบ O0/O2และระบุ transformations 5 จุดโดยมี disassembly evidence.
25. ทำ stripped reconstructionก่อนเปิด source: function purpose, inputs, outputs, branches.
26. เปิด sourceทีหลังและบันทึก assumptionsผิดอย่างน้อย 3 จุด.
27. อธิบายว่าทำไม source functionหนึ่งอาจไม่มี standalone functionใน O2.

## F. Tool Engineering

28. รัน binary-reportกับ non-ELFและพิสูจน์ว่า required tool failureทำ command non-zero.
29. รัน unit testsของ CFG parserและอธิบาย synthetic sampleแต่ละ case.
30. เพิ่ม testหนึ่งตัวสำหรับ CFG/tool limitationใหม่โดยไม่สร้าง false edge.
31. ขยาย report templateให้ทุก inferenceมี confidence/evidence reference.

## Practical submission

ส่ง authorized target hash, static triage, CFG, GDB evidence, pseudocode, facts/inferences/unknowns และ post-source comparison.

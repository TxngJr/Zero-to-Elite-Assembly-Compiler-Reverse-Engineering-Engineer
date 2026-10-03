# Common Mistakes

- รวมทุก phaseใน functionเดียวจน debugยาก
- compiler exit codeกับ generated program exit codeปนกัน
- optimized outputต่าง = bugทันที โดยไม่ดู semantics
- assembly linkได้ = compiler correct
- source invalidแล้วปล่อย tracebackแทน diagnostic
- testเฉพาะ return 42
- เพิ่ม syntaxแต่ลืม type/IR/backend/tests
- คิดว่า self-hostingจำเป็นก่อนเรียกสิ่งนี้ว่า compiler
- คิดว่า stack-slot backendไม่ใช่ compilerจริง

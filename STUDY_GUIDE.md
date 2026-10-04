# Study Guide

## วงจรการเรียนต่อหนึ่งหัวข้อ

1. **Read** — อ่าน mental model/vocabulary
2. **Predict** — เขียนผลที่คาดก่อนรัน
3. **Build** — compile/build พร้อมอธิบาย flags
4. **Run** — รัน controlled experiment
5. **Observe** — แยก observation จาก assumption
6. **Inspect** — ใช้ `file/readelf/objdump/GDB` หรือ toolของบท
7. **Debug** — หา first broken contract/representation
8. **Modify** — เปลี่ยนหนึ่งอย่างเพื่อทดสอบ mental model
9. **Explain** — สรุป why + limitation
10. **Assess** — exercises + practical modification + mastery rubric

## เส้นทางในทุก Chapter

```text
LEARNER_GUIDE
→ THEORY
→ WORKED_EXAMPLES
→ LABS
→ EXERCISES
→ MASTERY_TEST
→ RUBRIC
→ ANSWERS (เปิดหลังพยายามเอง)
```

## Evidence notebook

```text
notes/chXX/
├── predictions.md
├── commands.txt
├── observations.md
├── exercise-answers.md
├── modification.patch
└── mastery.md
```

ทุก experimentควรมี:

```text
Prediction:
Command/code:
Observed:
Expected invariant:
Why:
What may vary:
Modification:
Result:
Limitation:
```

## Mastery Gate

คะแนนเต็ม 100:
- concepts 20
- prediction 10
- lab evidence 20
- implementation/modification 25
- inspection/debugging 15
- explanation/limitations 10

ผ่านเมื่อ ≥85 พร้อม practical minimum ตาม `RUBRIC.md`.

`make test` ผ่านเป็น prerequisite ไม่ใช่คะแนน mastery.

## Capstone Gate

1. รัน automated baseline:
   ```bash
   make -C 18-capstone clean test
   ```
2. ทำ [18-capstone/ASSIGNMENT.md](18-capstone/ASSIGNMENT.md)
3. ส่ง compiler patch + OS patch/QEMU evidence + authorized RE report + defensive bug-fix report
4. ทำ oral/written defense

หลักสูตรจบเมื่อคุณสร้าง/เปลี่ยน/debug/อธิบายระบบได้ ไม่ใช่เมื่อ command เดียวขึ้น PASS.

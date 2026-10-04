# Course Authoring Standard

เอกสารนี้เป็น quality gate สำหรับทุก Chapter 00–18.

## หลักการ

หนึ่งบทจะถือว่า “พร้อมให้เรียนเอง” เมื่อไม่ได้มีแค่ theory + code แต่ต้องพาผู้เรียนผ่านวงจร:

```text
Why
→ Mental model
→ Worked example
→ Predict
→ Run
→ Observe
→ Explain
→ Modify
→ Break
→ Debug
→ Exercise
→ Mastery
```

## ไฟล์ขั้นต่ำต่อบท

- `README.md` — จุดประสงค์และ navigation
- `LEARNER_GUIDE.md` — ลำดับเรียนทีละขั้น
- `THEORY.md` — concepts
- `WORKED_EXAMPLES.md` — ตัวอย่างทำเต็มขั้นพร้อม expected evidence
- `LABS.md` — guided experiments
- `EXERCISES.md` — drills/questions
- `ANSWERS.md` — answer/hints
- `MASTERY_TEST.md` — assessment
- `RUBRIC.md` — scoring 100 points
- `COMMON_MISTAKES.md`
- `CHALLENGES.md`

## มาตรฐาน Worked Example

ทุก worked example ต้องมี:

1. **Goal**
2. **Prediction**
3. **Command / Code**
4. **Expected key evidence**
5. **What may vary**
6. **Explanation**
7. **Modification**
8. **Failure mode**
9. **Reflection**

ห้ามพึ่ง exact address/PID/tool version เว้นแต่โจทย์ต้องการ เพราะค่าพวกนี้เปลี่ยนได้ตาม environment.

## มาตรฐาน Exercise

ถ้าโจทย์เป็นหัวข้อสั้น เช่น `lexer vs parser` ผู้เรียนต้องตอบอย่างน้อย 4 ส่วน:

1. อธิบายด้วยภาษาตัวเอง
2. ยกตัวอย่างจาก project/course artifact
3. แสดง evidence ด้วย command/code/output
4. ระบุ misconception หรือกรณีขอบเขตหนึ่งอย่าง

ดังนั้น list หัวข้ออย่างเดียวไม่ถือว่าเสร็จจนตอบครบ 4 ส่วน.

## มาตรฐาน Mastery

คะแนนเต็ม 100:

- Concept model: 20
- Prediction/reasoning: 10
- Lab evidence: 20
- Implementation/modification: 25
- Inspection/debugging: 15
- Explanation/limitations: 10

ผ่านเมื่อ:
- รวม ≥85
- Implementation ≥18/25
- Lab evidence ≥14/20
- ไม่มี critical misconception ใน chapter gate

`make test` เป็นเพียง automated gate และไม่คิดแทนคะแนนความเข้าใจ.

## Claims policy

ใช้:
- “automated checks passed”
- “QEMU runtime boot gate passed”
- “tested on GCC/Clang”

หลีกเลี่ยง:
- “100% correct”
- “production ready”
- “fully verified”
- “elite/mastered” โดยไม่มี assessment evidence.

## Safety / authorization

Reverse engineering และ security labs จำกัดที่ course-owned / explicitly authorized targets และเน้น defensive analysis, fixing, regression, sanitizers และ fuzzing.

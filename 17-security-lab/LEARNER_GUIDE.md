# Learner Guide — Defensive Security Lab

## Why this chapter matters

ฝึก detect→root cause→fix→regression บน course-owned defects โดยไม่ข้ามไป weaponization.

## Study order

1. อ่าน `THEORY.md` เพื่อสร้าง vocabulary/mental model
2. ทำ `WORKED_EXAMPLES.md` โดยเขียน Prediction ก่อน Expected evidence
3. ทำ `LABS.md` และเก็บ command/output สำคัญ
4. รัน `make clean test` เพื่อเช็ก known regressions
5. ทำ `EXERCISES.md`: ทุกข้อให้ตอบ explanation + example + evidence + misconception
6. ทำ modification/local experimentอย่างน้อยหนึ่งจุด
7. ทำ `MASTERY_TEST.md` โดยไม่เปิด Answers
8. ให้คะแนนด้วย `RUBRIC.md`; ต่ำกว่า 85 ให้ retest weak area

## Evidence template

```text
Prediction:
Command/code:
Observed:
Expected key evidence:
Explanation:
What may vary:
Modification:
Result:
Limitation:
```

## Important

Automated testsพิสูจน์ implementationเฉพาะ cases ที่เขียนไว้ ไม่ได้พิสูจน์ mastery, production readiness หรือ completeness ของ subsystem.

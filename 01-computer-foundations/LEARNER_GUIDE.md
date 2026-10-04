# Learner Guide — Computer Foundations

## Why this chapter matters

ทำให้ binary/hex/signed/endian/memory เป็นของที่คำนวณได้ ไม่ใช่คำศัพท์.

## ลำดับเรียนที่แนะนำ

1. อ่าน `THEORY.md` รอบแรกเพื่อรู้ vocabulary โดยยังไม่จำทุกอย่าง
2. เปิด `WORKED_EXAMPLES.md` และ **เขียน Prediction ก่อนดู Expected evidence**
3. ทำ `LABS.md` ทีละข้อ เก็บ command/output ที่สำคัญ
4. รัน `make clean test` เพื่อเช็ก regression ของ repository
5. ทำ `EXERCISES.md` โดยตอบ 4 ส่วน: explanation, example, evidence, misconception
6. ทำ modification อย่างน้อยหนึ่งจุดใน local copy แล้วทำนายผลก่อนรัน
7. ทำ `MASTERY_TEST.md` โดยไม่เปิด `ANSWERS.md`
8. ให้คะแนนด้วย `RUBRIC.md`; ถ้าต่ำกว่า 85 ให้ย้อนเฉพาะ weak area

## Evidence ที่ควรเก็บ

```text
Prediction:
Command/code:
Observed:
Expected key evidence:
Why:
What varied on my machine:
Modification:
Result:
Remaining question:
```

## Rule สำหรับคนเริ่มจากศูนย์

ถ้าคำศัพท์หนึ่งยังอธิบายด้วยประโยคของตัวเองไม่ได้ **อย่ารีบข้ามไปบทถัดไป**. กลับไปสร้างตัวอย่างเล็กที่สุดที่เห็น concept นั้นได้.

## Automated test ≠ mastery

`make test` บอกว่า known regression tests ผ่าน ไม่ได้บอกว่าคุณสร้าง/debug สิ่งนี้จาก blank file ได้. Chapter ผ่านเมื่อ practical evidence + mastery rubric ผ่านด้วย.

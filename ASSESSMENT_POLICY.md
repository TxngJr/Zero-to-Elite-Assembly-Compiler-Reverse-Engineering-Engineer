# Assessment Policy

## ทำไมต้องแยก tests กับ mastery

`make test` ตอบคำถามว่า:

> implementation ที่ repository รู้จักยังทำงานตาม regression tests หรือไม่?

มันไม่ตอบว่า:

> ผู้เรียนอธิบายเหตุผลได้หรือไม่?
> เขียนใหม่จาก blank file ได้หรือไม่?
> debug failure ใหม่ได้หรือไม่?

ดังนั้นทุกบทใช้ rubric 100 คะแนน.

## Evidence package ต่อบท

แนะนำสร้าง:

```text
notes/chXX/
├── predictions.md
├── commands.txt
├── observations.md
├── exercise-answers.md
├── modification.patch
└── mastery.md
```

## Practical gate

อย่างน้อยหนึ่งงานต้องแก้/สร้าง code ด้วยตัวเอง ไม่ใช่แค่รัน solution ที่มีอยู่.

## Retest

ถ้าไม่ผ่าน:
1. ระบุข้อที่ผิด
2. กลับไป worked example/lab ที่เกี่ยวข้อง
3. ทำ variation ใหม่
4. retest เฉพาะ weak area
5. ทำ mastery ใหม่โดยไม่เปิด answers

## Capstone

Chapter 18 ต้องมีทั้ง automated audit และ human deliverables/report; การรัน `make test` อย่างเดียวไม่ถือว่าจบหลักสูตร.

# Rubric — C Machine Model

คะแนนเต็ม 100. เกณฑ์ผ่านปกติ **≥85** และต้องผ่าน practical minimum.

| หมวด | คะแนน | หลักฐาน |
|---|---:|---|
| Mental model / concepts | 20 | อธิบายคำสำคัญและความสัมพันธ์โดยไม่คัด Theory |
| Prediction / reasoning | 10 | prediction ก่อน lab อย่างน้อย 3 จุด |
| Lab evidence | 20 | command/output/observation ที่ตรวจย้อนกลับได้ |
| Implementation / modification | 25 | แก้หรือสร้าง code/config ใน local copyและมี test |
| Inspection / debugging | 15 | ใช้ tools ของบทเพื่อพิสูจน์ state/artifact |
| Explanation / limitations | 10 | อธิบาย why + สิ่งที่ test ยังพิสูจน์ไม่ได้ |

## Practical minimum

- Implementation / modification ≥18/25
- Lab evidence ≥14/20
- ไม่มี critical misconception ที่ทำให้บทถัดไปผิดฐาน

## หักคะแนนแรง

- รัน solution แล้วส่ง output โดยไม่มี prediction/explanation
- อ้าง observation หนึ่งครั้งเป็น universal rule
- ใช้ exact address/PID เป็นคำตอบโดยไม่อธิบาย semantics
- บอกว่า `make test` ผ่านจึงเข้าใจบทแล้ว

## Retest

ถ้าไม่ผ่าน ให้เลือก 2 weak categories, ทำ variation ใหม่ใน `WORKED_EXAMPLES.md` หรือ `LABS.md`, แล้วสอบ mastery ใหม่โดยไม่เปิด Answers.

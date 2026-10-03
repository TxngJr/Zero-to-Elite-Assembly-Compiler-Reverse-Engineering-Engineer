# Study Guide

## วงจรการเรียนต่อหนึ่งหัวข้อ

1. **Read** — อ่านแนวคิดให้จบหนึ่งช่วง
2. **Predict** — เขียนสิ่งที่คิดว่าจะเกิดก่อนรัน
3. **Build** — compile/build ด้วยคำสั่งที่อธิบายได้
4. **Run** — รันและบันทึก output สำคัญ
5. **Observe** — แยก observation ออกจาก assumption
6. **Inspect** — ใช้ `file`, `readelf`, `objdump`, GDB หรือการดู raw bytes ตามบท
7. **Debug** — เมื่อผิด ให้หาสาเหตุ ไม่ลบ error แล้วข้าม
8. **Modify** — เปลี่ยน input/code หนึ่งอย่างเพื่อพิสูจน์ mental model
9. **Explain** — สรุปด้วยภาษาของตัวเอง
10. **Test** — ทำ exercise/challenge และ mastery test

## สมุดทดลองที่แนะนำ

สร้างนอก repo หรือในพื้นที่ส่วนตัว:

```text
notes/
predictions/
experiments/
```

สำหรับแต่ละ lab ให้จด:

```text
Prediction:
Observed:
Why:
Evidence:
What I changed:
What I still do not understand:
```

## อย่าเรียนแบบ copy/paste

Copy command ได้เมื่อต้องลดงานพิมพ์ แต่คุณต้องตอบได้ว่า option สำคัญแต่ละตัวทำอะไร ตัวอย่าง `gcc -S -O0 -g` ต้องรู้ว่า `-S`, `-O0`, `-g` เปลี่ยน pipeline อย่างไร

## Mastery Gate

ให้ผ่าน chapter เมื่อ:

- คำถามแนวคิดถูกอย่างน้อย ~85%
- required labs/build/tests ผ่าน
- อธิบายผลโดยอาศัย evidence ได้
- สามารถเปลี่ยนตัวอย่างเล็กน้อยแล้วทำนายผลใหม่ได้

คำถามเชิงอธิบายเป็น self-assessment ไม่ควรหลอกตัวเองด้วยการจำเฉลย

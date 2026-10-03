# Challenges

## Challenge 01-A — Permission byte design
ออกแบบ 8-bit flags สำหรับ READ, WRITE, EXEC, ADMIN, AUDIT, ARCHIVE และ reserved 2 bits. ระบุ masks และ encode READ|WRITE|AUDIT.

## Challenge 01-B — Decode a byte stream
จาก `34 12 EF BE AD DE 41 00` ตีความ 2 bytesแรกเป็น LE uint16, 4 ถัดไป LE uint32, 2 สุดท้ายเป็น char sequence.

## Challenge 01-C — Design a tiny 8-bit ISA
กำหนด encoding ของ LOADI, ADD, STORE, JMP, HALT ภายใน 8/16-bit instruction format, ระบุ limitations และ simulate 2+3. ห้ามเรียกว่า x86.

## Challenge 01-D — Predict before inspect
เลือก 10 integer constants, เขียน bytes ที่คาดบน x86-64 little endian สำหรับ 16/32/64 bit แล้วใช้ Memory Viewer ตรวจ.

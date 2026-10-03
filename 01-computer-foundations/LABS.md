# Labs

## Lab 01-01 — Binary by hand
แปลง 13,42,65,127,128,200,255 เป็น 8-bit binary ด้วยมือก่อนตรวจด้วย `show_integer_bits`.

## Lab 01-02 — Hex ↔ Binary
แปลง `0x0F,0x41,0x7F,0x80,0xA7,0xFF,0x100,0xDEADBEEF` โดยจับกลุ่ม nibble.

## Lab 01-03 — Same bits, different interpretation
ใช้ `signed_unsigned.c` กับ `0x00,0x01,0x7F,0x80,0xFB,0xFF`; ทำนาย unsigned/signed values.

## Lab 01-04 — Bit masks
กำหนด READ=bit0, WRITE=bit1, EXEC=bit2, ADMIN=bit3. สร้าง/clear/test combinations ด้วยมือและ code.

## Lab 01-05 — Endianness
ก่อนรัน `endianness.c` วาด bytes ของ `0x12345678`; เทียบ prediction.

## Lab 01-06 — Memory bytes
ใช้ `show_bytes.c` กับ uint16/32/64; บันทึก address,size,bytes โดยไม่เรียก address ว่า physical.

## Lab 01-07 — ASCII
หา decimal/hex ของ A,a,0,newline,space และเทียบ numeric digit กับ character code.

## Lab 01-08 — Binary Playground
Build project และทดสอบ 0,65,255,256; อธิบาย width.

## Lab 01-09 — Memory Viewer
ตรวจ integer หลายขนาดและ struct. แยก bytes ที่เห็นจาก meaning.

## Lab 01-10 — CPU paper simulation
```text
R1=3 R2=5 PC=0
0: ADD R1,R2
1: STORE [100],R1
2: HALT
```
เขียน state หลังแต่ละ fictional instruction.

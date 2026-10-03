# Theory — Computer Foundations

## 1. Information as bits
Bit เป็นหน่วยเชิงนามธรรมที่มีสองค่า 0/1. Hardware จริงอาจ encode สองสถานะด้วยระดับแรงดัน, charge, magnetic orientation หรือกลไกอื่นตาม technology; อย่าลดคำอธิบายเป็น “transistor หนึ่งตัว = หนึ่ง bit” แบบสากล

Pattern เดียวกันตีความต่างกันได้ เช่น `01000001` อาจเป็น integer 65 หรือ ASCII `'A'` ขึ้นกับ context.

## 2. Units
บนแพลตฟอร์มเป้าหมายทั่วไป:
```text
1 nibble = 4 bits
1 byte   = 8 bits
16 bits  = 2 bytes
32 bits  = 4 bytes
64 bits  = 8 bytes
```
ใน C byte คือหน่วยที่ `sizeof(char)==1`; จำนวน bits มาจาก `CHAR_BIT`. คำว่า word ขึ้นกับ architecture/context.

## 3. Positional notation
`101101₂ = 1×2^5 + 0×2^4 + 1×2^3 + 1×2^2 + 0×2 + 1 = 45`.

Powers of two ที่ควรคล่อง: 1,2,4,8,16,32,64,128,256,512,1024.

## 4. Decimal ↔ Binary
ใช้การหาร 2 ซ้ำหรือแตกค่าเป็นผลรวม powers of two. เช่น 13=8+4+1 → `1101₂`.

## 5. Hexadecimal
หนึ่ง hex digit พอดีกับ 4 bits:
```text
0=0000 1=0001 2=0010 3=0011
4=0100 5=0101 6=0110 7=0111
8=1000 9=1001 A=1010 B=1011
C=1100 D=1101 E=1110 F=1111
```
ดังนั้น `1101 1110 1010 1101 1011 1110 1110 1111 = 0xDEADBEEF`. Hex เป็น notation ไม่ใช่ข้อมูลชนิดใหม่.

## 6. Unsigned integers
n-bit unsigned มี `2^n` patterns และ range `0 ... 2^n - 1`. 8 bits → 0..255.

## 7. Two's complement
n-bit signed two's-complement range:
```text
-2^(n-1) ... 2^(n-1)-1
```
8 bits → -128..127. Pattern `11111111` คือ 255 unsigned แต่ -1 signed. ถ้า MSB=1 วิธีหนึ่งคือ `signed = unsigned - 2^n`.

## 8. Overflow: hardware vs C
Unsigned arithmetic ใน C ใช้ modulo `2^n` ตาม width. Signed overflow ใน C เป็น undefined behavior; อย่าสรุปจาก CPU observation ว่า signed C ต้อง wrap เสมอ. Carry/overflow flags เป็น ISA concepts ที่จะเรียนลึกภายหลัง.

## 9. Bitwise operations
```text
A B | AND OR XOR
0 0 |  0   0   0
0 1 |  0   1   1
1 0 |  0   1   1
1 1 |  1   1   0
```
NOT กลับแต่ละ bit.

## 10. Masks
```c
flags |= mask;
flags &= ~mask;
flags ^= mask;
if (flags & mask) { }
```
สำหรับ field หลาย bits ใช้ mask + shift.

## 11. Shifts
Left shift เลื่อนไป weight สูงขึ้น; logical right shift เติม 0. Shortcut “shift = multiply/divide” ใช้ได้เมื่อกฎ type/width/overflow รองรับ โดยเฉพาะ C signed expressions ต้องระวัง UB.

## 12. Characters and encodings
ASCII: `'A'=65=0x41=01000001`, `'0'=48=0x30`, newline=10. UTF-8 ใช้ 1–4 bytes ต่อ code point โดย ASCII เป็น subset; “หนึ่ง character=หนึ่ง byte” ไม่ใช่กฎทั่วไป.

## 13. Memory as addressed bytes
```text
Address   Byte
0x1000    41
0x1001    42
0x1002    43
0x1003    00
```
Object หลาย byte ครอบ address range. Address ที่ user process เห็นทั่วไปเป็น virtual address ไม่ใช่ physical RAM address โดยตรง.

## 14. Endianness
`0x12345678` เป็น 32-bit:
```text
Little endian: 78 56 34 12
Big endian:    12 34 56 78
```
x86-64 ใช้ little endian สำหรับ integer memory representation. Endianness ไม่ได้หมายถึงการกลับ bits ภายใน byte.

## 15. Alignment
Address ที่ align 4 bytes มักหาร 4 ลงตัว เช่น 0x1000,0x1004. Alignment เกี่ยวกับ ABI/hardware/performance. อย่าสรุปว่า unaligned access “ใช้ไม่ได้ทุก architecture”; x86-64 รองรับหลายกรณี.

## 16. CPU high-level model
```text
           ┌──────── CPU ────────┐
Memory ⇄   │ Registers           │
           │ ALU                 │
           │ Control / Decode    │
           │ Instruction pointer │
           └─────────────────────┘
```

## 17. Instructions
Instruction คือ operation ที่ ISA encode. ตัวอย่าง fictional:
```text
LOAD R1, [100]
ADD  R1, R2
STORE [200], R1
```
ไม่ใช่ x86 syntax จริง.

## 18. Fetch → Decode → Execute
```text
Fetch instruction bytes
        ↓
Decode operation/operands
        ↓
Execute / memory / update state
        ↓
Choose next instruction
```
CPU จริงมี pipeline, out-of-order, speculation, caches ฯลฯ จึงไม่ใช่ timing model จริง.

## 19. Source to execution
```text
Source → toolchain → executable bytes → loader/kernel → process virtual memory → CPU
```
Chapter 02 จะวาง C objects/pointers บน model นี้.

# Worked Examples — Computer Foundations

เป้าหมายคือคำนวณเองก่อนให้โปรแกรมยืนยัน.

## Example 1 — Decimal ↔ Binary ↔ Hex

**Goal:** แปลง 173 ด้วยมือ.

**Prediction / calculation:**

```text
173 = 128 + 32 + 8 + 4 + 1
    = 10101101₂
    = 0xAD
```

**Command / action:**

```bash
make -C 01-computer-foundations clean all
01-computer-foundations/build/show_integer_bits 173
```

ถ้า Makefileสร้าง binaryชื่ออื่น ให้รัน `make -C 01-computer-foundations test` แล้วดู commandที่ใช้.

**Expected key evidence:** binary pattern `10101101` และ hex `AD`/equivalent formatting.

**What may vary:** spacing/prefix `0x`.

**Explain:** hex digitหนึ่งตัวแทน 4 bits; `1010 1101 → A D`.

**Modification:** ทำ 0, 127, 128, 255 โดยไม่ดูเครื่องก่อน.

**Failure mode:** อย่าสับสน “hex representation” กับค่าชนิดใหม่ใน memory.

**Reflection:** อธิบายว่าทำไม byteเดียวกัน `0xFF` อาจตีความ 255 หรือ -1.

---

## Example 2 — Same byte, signed vs unsigned

**Goal:** เห็น two's-complement interpretation.

**Command / action:**

```bash
gcc -std=c17 -Wall -Wextra -Wpedantic -g \
  01-computer-foundations/examples/signed_unsigned.c \
  -o /tmp/signed_unsigned

/tmp/signed_unsigned
```

**Prediction:** pattern `11111011` / `0xFB` คือ 251 unsigned และ -5 signed 8-bit.

**Expected key evidence:** โปรแกรมแสดง bit patternเดียวแต่ค่าต่างตาม signedness.

**What may vary:** formatting.

**Explain:** ถ้า high bit=1 ใน n-bit two's complement, signed value = unsigned value - `2^n`.

**Modification:** คำนวณ `0x80`, `0x7F`, `0xFF` ก่อนรัน.

**Failure mode:** อย่าอ้างว่า “stored byteรู้ว่าตัวเอง signed”; signednessมาจาก interpretation/type operations.

**Reflection:** สรุป rangeของ int8/uint8.

---

## Example 3 — Endianness จาก memoryจริง

**Goal:** ทำนาย byte orderของ `0x12345678` บน x86-64.

**Prediction:**

```text
lowest address → 78 56 34 12
```

**Command / action:**

```bash
gcc -std=c17 -Wall -Wextra -Wpedantic -g \
  01-computer-foundations/examples/endianness.c \
  -o /tmp/endianness

/tmp/endianness
```

**Expected key evidence:** least-significant byteอยู่ addressต่ำสุด.

**What may vary:** object address.

**Explain:** little-endianเรียง bytes ไม่ได้กลับ bitsภายใน byte.

**Modification:** เปลี่ยน local copyเป็น `0xDEADBEEF` แล้วทำนาย `EF BE AD DE`.

**Failure mode:** อย่า dereference arbitrary address; inspect objectที่โปรแกรมเป็นเจ้าของ.

**Reflection:** reconstruct integerจาก bytes `34 12 00 00` บน little-endian.

---

## Example 4 — Bit masks as state

**Goal:** ใช้ bitsเป็น flagsโดยไม่ทำลาย bitsอื่น.

**Command / action:**

```bash
gcc -std=c17 -Wall -Wextra -Wpedantic -g \
  01-computer-foundations/examples/bit_masks.c \
  -o /tmp/bit_masks
/tmp/bit_masks
```

**Prediction:** `OR` set bit, `AND ~mask` clear, `XOR` toggle, `AND` test.

**Expected key evidence:** operationsเปลี่ยนเฉพาะ bitsตาม mask.

**What may vary:** numeric flagsเริ่มต้นใน example.

**Explain:** truth tableของ AND/OR/XORเชื่อมตรงกับ behaviorของ mask.

**Modification:** กำหนด READ=bit0, WRITE=bit1, EXEC=bit2, ADMIN=bit3แล้วสร้าง permission `READ|EXEC`.

**Failure mode:** `!value` เป็น logical NOT ไม่ใช่ bitwise `~value`.

**Reflection:** ออกแบบ maskสำหรับ field bits 2..5 และวิธี extract.

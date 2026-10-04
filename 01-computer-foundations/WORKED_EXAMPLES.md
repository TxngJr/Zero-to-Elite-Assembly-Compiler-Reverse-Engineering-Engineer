# Worked Examples — Computer Foundations

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — 173 → binary → hex

**Goal:** 173 → binary → hex

**Prediction:** แปลงด้วยมือก่อนใช้ tool

**Command / action:**

```text
173 = 128+32+8+4+1
```

**Expected key evidence:** 10101101₂ = 0xAD.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปลี่ยนเป็น 200 แล้วทำโดยไม่ใช้ calculator.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Same bits, different meaning

**Goal:** Same bits, different meaning

**Prediction:** ทำนาย 11111011 เป็น unsigned และ signed 8-bit

**Command / action:**

```text
run signed_unsigned example
```

**Expected key evidence:** 251 unsigned และ -5 signed.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** อธิบายสูตร unsigned-256 เมื่อ bit7=1.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — Little endian

**Goal:** Little endian

**Prediction:** วาด bytes ของ 0x12345678 ก่อนรัน

**Command / action:**

```text
run endianness example
```

**Expected key evidence:** x86-64 memory bytes: 78 56 34 12.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** reconstruct 0xDEADBEEF จาก EF BE AD DE.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


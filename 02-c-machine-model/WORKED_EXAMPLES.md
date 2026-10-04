# Worked Examples — C Machine Model

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — Array and pointer addresses

**Goal:** Array and pointer addresses

**Prediction:** ทำนาย stride ของ int array

**Command / action:**

```text
พิมพ์ &a[0], &a[1], sizeof(int)
```

**Expected key evidence:** address difference เท่ากับ sizeof(int) บน build นี้.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปลี่ยน type เป็น long long และเปรียบเทียบ.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Struct layout

**Goal:** Struct layout

**Prediction:** ทำนาย offsets/padding ก่อน sizeof

**Command / action:**

```text
ใช้ offsetof + sizeof กับ struct lab
```

**Expected key evidence:** offsets ต้องสอดคล้อง alignment; size อาจมี tail padding.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** สลับ field order แล้ววัด size ใหม่.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — Undefined behavior evidence

**Goal:** Undefined behavior evidence

**Prediction:** แยก language rule ออกจาก observation

**Command / action:**

```text
build example ทั้ง -O0 และ -O2
```

**Expected key evidence:** ผลที่ต่างกันไม่ทำให้ UB มี semantics ใหม่.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** อธิบายว่าทำไม observation ไม่ใช่ guarantee.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


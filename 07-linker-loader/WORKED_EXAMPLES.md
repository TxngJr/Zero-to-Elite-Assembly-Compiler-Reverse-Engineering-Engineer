# Worked Examples — Linker & Loader

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — Relocation resolution

**Goal:** Relocation resolution

**Prediction:** ตาม symbol จาก .o ไป executable

**Command / action:**

```text
nm/readelf/objdump -dr
```

**Expected key evidence:** relocation ใน object เปลี่ยนเป็น address/indirection หลัง link.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** ย้าย function ไปอีก object แล้วเทียบ.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Static vs shared

**Goal:** Static vs shared

**Prediction:** เปรียบเทียบ dependencies

**Command / action:**

```text
file; ldd; readelf -d
```

**Expected key evidence:** shared build มี dynamic dependencies; static demo ต่าง.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** วัด file size และอธิบายเหตุผล.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — PLT/GOT call

**Goal:** PLT/GOT call

**Prediction:** ตาม external call path

**Command / action:**

```text
objdump -d; readelf -rW
```

**Expected key evidence:** call อาจผ่าน PLT และ GOT relocation.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** ใช้ LD_DEBUG ใน local demoแล้วบันทึก observation.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


# Worked Examples — ELF Internals

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — Section vs segment

**Goal:** Section vs segment

**Prediction:** ทำนายว่า .text อยู่ใน LOAD segment ใด

**Command / action:**

```text
readelf -SW; readelf -lW
```

**Expected key evidence:** section เป็น tooling/link view; segment เป็น loader view.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** ใช้ mapping tableจาก readelf -lW.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Symbols

**Goal:** Symbols

**Prediction:** แยก local/global/undefined

**Command / action:**

```text
nm -an object; readelf -sW
```

**Expected key evidence:** undefined symbol ใน .o อาจถูก resolve ตอน link.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปรียบเทียบ object กับ executable.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — Relocation

**Goal:** Relocation

**Prediction:** หาตำแหน่งที่ linker ยังต้องแก้

**Command / action:**

```text
readelf -rW object
```

**Expected key evidence:** relocation แสดง offset/type/symbol.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** แก้ sourceให้เพิ่ม external reference แล้วเทียบ.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


# Worked Examples — x86-64 Assembly

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — EAX zero-extension

**Goal:** EAX zero-extension

**Prediction:** ทำนาย RAX หลังเขียน EAX

**Command / action:**

```text
mov rax,-1; mov eax,5
```

**Expected key evidence:** RAX = 5 เพราะ write 32-bit zeroes upper half.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปลี่ยน eax เป็น ax แล้วอธิบาย upper bits.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Signed vs unsigned branch

**Goal:** Signed vs unsigned branch

**Prediction:** ใช้ค่า bit pattern เดียวแล้วเปรียบเทียบ jl กับ jb

**Command / action:**

```text
cmp operands แล้ว inspect flags/GDB
```

**Expected key evidence:** CF/OF/SF/ZF ถูกตีความต่างกันตาม jcc.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** สร้าง input ที่ signed negative แต่ unsigned large.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — Array loop

**Goal:** Array loop

**Prediction:** ตาม index/address/accumulator ทีละ iteration

**Command / action:**

```text
GDB si + info registers + x/
```

**Expected key evidence:** scale ต้องตรง element width.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปลี่ยน int32 เป็น int64 แล้วแก้ addressing scale.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


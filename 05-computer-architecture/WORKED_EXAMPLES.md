# Worked Examples — Computer Architecture

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — Direct-mapped cache

**Goal:** Direct-mapped cache

**Prediction:** คำนวณ tag/index/offset ด้วยมือ

**Command / action:**

```text
run cache-sim กับ address sequence
```

**Expected key evidence:** hit/miss ต้องตรง mapping model.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปลี่ยน line size แล้วทำนายใหม่.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — 2-bit branch predictor

**Goal:** 2-bit branch predictor

**Prediction:** ตาม state transitions ของ branch pattern

**Command / action:**

```text
run branch-predictor
```

**Expected key evidence:** state saturates และ prediction เปลี่ยนตาม counter.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** ทดลอง TTTNT pattern.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — Tiny CPU

**Goal:** Tiny CPU

**Prediction:** trace fetch/decode/execute state

**Command / action:**

```text
run tiny-cpu with short program
```

**Expected key evidence:** PC/register/memory เปลี่ยนตาม instruction semantics.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เพิ่ม instruction หนึ่งแบบแล้วเขียน test.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


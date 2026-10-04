# Worked Examples — Compiler Frontend

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — Precedence AST

**Goal:** Precedence AST

**Prediction:** ทำนาย AST ของ 1+2*3

**Command / action:**

```text
--tokens และ --ast บนโปรแกรมเล็ก
```

**Expected key evidence:** root เป็น + และ right child เป็น *.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** แก้ expression เป็น (1+2)*3 แล้วเทียบ.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Semantic rejection

**Goal:** Semantic rejection

**Prediction:** แยก syntax-valid กับ type-invalid

**Command / action:**

```text
--check program ที่ let bool = 42
```

**Expected key evidence:** parser ผ่านแต่ checker reject type.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** สร้าง wrong arity และ unknown variable เพิ่ม.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — Entry ABI contract

**Goal:** Entry ABI contract

**Prediction:** ทดสอบ main signature

**Command / action:**

```text
--check bad_main_args.el
```

**Expected key evidence:** ต้อง reject และบอก fn main() -> int.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** อธิบายว่าทำไม hosted runtime ต้องมี contract ชัด.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


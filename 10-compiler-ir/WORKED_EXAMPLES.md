# Worked Examples — Compiler IR

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — Diamond CFG and dominators

**Prediction:** วาด entry/then/else/join และทำนาย dominator sets.

**Action:**
```text
run test_ir.py หรือ --dom กับ diamond.el
```

**Expected key evidence:** join ถูก dominate โดย entry แต่ไม่ถูก dominate โดย then/else.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เพิ่ม block ก่อน join แล้วคำนวณใหม่.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — Liveness

**Prediction:** ทำนาย live-in/live-out ของ block ที่คำนวณ y=x+b แล้ว return y.

**Action:**
```text
run semantic unit test
```

**Expected key evidence:** live-in ต้องมีค่าที่ใช้ก่อน define; live-out exit เป็น empty.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เพิ่ม successor ที่ใช้ x แล้วดู set เปลี่ยน.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Exact constant folding

**Prediction:** ทำนาย INT64_MAX/3 โดยไม่ใช้ float.

**Action:**
```text
--opt large integer case
```

**Expected key evidence:** ผลต้องเป็น 3074457345618258602 และ optimized/unoptimized semantics ตรงกัน.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** ทดสอบ INT64_MIN/-1 ว่าต้องไม่ fold trap หาย.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


# Worked Examples — My Compiler — EliteC

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — Intermediate emits

**Prediction:** ทำนาย representation ของ tokens/AST/IR/asm.

**Action:**
```text
elitec --emit tokens|ast|ir|asm example.el
```

**Expected key evidence:** แต่ละ mode หยุดที่ phase boundary ต่างกัน.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** สร้าง source errorแล้วดูว่า phase ไหน reject.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — Optimized vs unoptimized

**Prediction:** ทำนายว่าผล executable ต้องเหมือนกัน.

**Action:**
```text
compile large_div.el ทั้ง --opt และ no-opt
```

**Expected key evidence:** ทั้งคู่ exit 0; IR อาจต่างแต่ semantics ต้องตรง.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เพิ่ม boundary arithmetic case.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Run status separation

**Prediction:** ทำนาย elitec status เมื่อโปรแกรม return 42.

**Action:**
```text
elitec --run return42.el
```

**Expected key evidence:** driver รายงาน program status 42 แต่ตัว compiler commandสำเร็จ; --propagate-exit-code จึงค่อยคืน 42.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** อธิบายว่าทำไม CI ต้องแยกสอง status.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


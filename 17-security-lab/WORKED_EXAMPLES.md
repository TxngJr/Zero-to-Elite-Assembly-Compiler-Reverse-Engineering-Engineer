# Worked Examples — Defensive Security Lab

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — Bounds defect

**Prediction:** ทำนายสอง check ที่ length-prefixed parserต้องมี.

**Action:**
```text
make sanitizer-demo
```

**Expected key evidence:** ASan จับ course-injected OOB; fixed pathเช็ก input_remaining และ capacity.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เพิ่ม boundary max/max+1 regression.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — Lifetime and format

**Prediction:** แยก runtime lifetime defectกับ compile-time format defense.

**Action:**
```text
make sanitizer-demo; make -C projects/format-lab unsafe-check
```

**Expected key evidence:** ASan จับ UAF และ compiler reject non-literal format target.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** อธิบายว่าทำไม hardeningไม่แทน ownership/bounds fix.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Coverage-guided fuzzing

**Prediction:** แยก random smokeกับ libFuzzer.

**Action:**
```text
make fuzz
```

**Expected key evidence:** libFuzzerใช้ corpus/coverage; no crashไม่ใช่ security proof.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เพิ่ม seed valid edge caseและเก็บ regressionถ้าพบ failure.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


# Worked Examples — Compiler Backend

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — Stack-slot frame

**Prediction:** นับ virtual values แล้วทำนาย frame size/alignment.

**Action:**
```text
emit asm ของ simple function
```

**Expected key evidence:** prologue push rbp/mov rbp,rsp และ frame rounded เป็น 16-byte multiple.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เพิ่ม locals แล้วดู frame size.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — Eight-argument call

**Prediction:** ทำนาย register/stack placement.

**Action:**
```text
emit asm sum8
```

**Expected key evidence:** args 1–6 ไป register; 7–8 ถูก push และ cleanup หลัง call.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เปลี่ยนเป็น 7/9 args แล้วตรวจ padding.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Signed division

**Prediction:** ทำนาย cqo/idiv state.

**Action:**
```text
emit asm ของ / และ %
```

**Expected key evidence:** division ใช้ RDX:RAX และ remainder อยู่ RDX.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** ใช้ negative operandsแล้วเทียบกับ language spec.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


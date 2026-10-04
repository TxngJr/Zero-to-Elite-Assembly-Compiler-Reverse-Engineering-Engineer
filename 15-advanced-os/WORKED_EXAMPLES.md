# Worked Examples — Advanced OS

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — Round-robin

**Prediction:** ทำนาย schedule ของ bursts 5,3,4 quantum=2.

**Action:**
```text
run scheduler-sim
```

**Expected key evidence:** รวม ticks=12 และแต่ละ taskได้ sliceตาม queue.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เพิ่ม BLOCKED stateใน local variation.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — Copy-on-write

**Prediction:** ทำนาย refcountก่อน/หลัง child write.

**Action:**
```text
run vm-cow-sim
```

**Expected key evidence:** หลัง fork shared frame refs=2; child writeสร้าง frameใหม่.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** อธิบาย page-fault condition ที่ kernelจริงต้องตรวจ.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Pipe + VFS

**Prediction:** trace circular buffer wrap และ /etc/motd path components.

**Action:**
```text
run ipc-sim และ vfs-sim
```

**Expected key evidence:** count/head/tail และ directory traversalตรง invariant.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เพิ่ม nested directoryหรือ wrap-around case.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


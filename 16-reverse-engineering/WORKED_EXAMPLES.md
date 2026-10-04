# Worked Examples — Reverse Engineering

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — O0 vs O2

**Prediction:** ทำนายว่าฟังก์ชัน/stack localsจะเปลี่ยนอย่างไร.

**Action:**
```text
build challenge suite; objdump control-o0/control-o2
```

**Expected key evidence:** O2 อาจ inline/simplify/reorder; semanticsยังเทียบได้.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เขียน facts/inferencesแยกสองคอลัมน์.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — Real CFG blocks

**Prediction:** ทำนาย leaders จาก branch targets/fallthrough.

**Action:**
```text
cfg_extract.py control-o0 และ --json
```

**Expected key evidence:** output มี function, basic blocks, branch/fallthrough edges และ calls.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เลือก loop binaryแล้วระบุ back edge.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Stripped reconstruction

**Prediction:** ห้ามเปิด sourceก่อนเขียน pseudocode.

**Action:**
```text
file/readelf/objdump/GDB control-stripped
```

**Expected key evidence:** symbol namesหายบางส่วนแต่ code/ELF evidenceยังอยู่.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เปิด sourceทีหลังแล้วบันทึก assumptions ที่ผิด.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


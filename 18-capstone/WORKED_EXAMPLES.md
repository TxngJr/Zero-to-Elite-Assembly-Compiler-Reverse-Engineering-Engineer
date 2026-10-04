# Worked Examples — Final Capstone

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — Source to executable evidence

**Prediction:** ทำนาย artifacts ที่เปลี่ยนทุก phase.

**Action:**
```text
make clean test แล้ว inspect capstone.ir/s/dis
```

**Expected key evidence:** IR/asm/ELFเป็น representationต่างกันและ executable behaviorต้องผ่าน.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** reconstruct capstone-appก่อนเปิด source.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — Kernel evidence

**Prediction:** แยก static kernel-image checkกับ runtime boot gate.

**Action:**
```text
inspect eliteos64-kernel.elf และรัน Chapter14 qemu-test
```

**Expected key evidence:** static ELF/Multibootไม่ได้แทน PIT runtime; QEMU gateต้องเห็น pit irq ok.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เขียน limitationsว่าฟีเจอร์ Chapter15ยังเป็น simulator.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Defensive report

**Prediction:** สร้าง claimที่ทุกประโยคมี evidence.

**Action:**
```text
กรอก REPORT_TEMPLATE + manifest hashes
```

**Expected key evidence:** reportแยก observed/inferred/unknownและระบุ toolchain/commit.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** ให้คนอื่น challenge claimหนึ่งข้อแล้วหาหลักฐานเพิ่ม.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


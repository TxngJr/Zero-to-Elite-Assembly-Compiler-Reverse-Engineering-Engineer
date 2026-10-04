# Worked Examples — OS Foundations

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — Virtual-address split

**Prediction:** แยก PML4/PDPT/PD/PT/offset จาก address.

**Action:**
```text
page_walk.py split 0x7fffffffffff
```

**Expected key evidence:** indices ต้องอยู่ 0..511 และ offset 0..4095.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** ลอง non-canonical address แล้วอธิบาย rejection.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — IDT gate encoding

**Prediction:** ทำนาย 16-byte gate fields จาก handler address.

**Action:**
```text
run descriptor-lab
```

**Expected key evidence:** decode กลับต้องได้ handler/selector/attributes เดิม.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เปลี่ยน handler address แล้วคำนวณ low/mid/high.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Long-mode checklist

**Prediction:** เรียง CR4.PAE, CR3, EFER.LME, CR0.PG, GDT/far transfer.

**Action:**
```text
เขียน sequence ก่อนเปิด Chapter14 boot.s
```

**Expected key evidence:** order ต้องมี tablesพร้อมก่อน enable paging.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** อธิบาย failure mode ถ้า CR3 ชี้ผิด.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


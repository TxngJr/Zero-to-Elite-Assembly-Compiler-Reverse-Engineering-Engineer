# Worked Examples — My OS — EliteOS64

ใช้ Predict → Run → Observe → Explain → Modify. อย่าเทียบ exact address/PID/version ถ้าไม่ใช่ invariant.

## Example 1 — Boot runtime milestones

**Prediction:** ทำนาย marker ที่ควรเห็นก่อน shell.

**Action:**
```text
make qemu-test
```

**Expected key evidence:** serial log ต้องถึง [BOOT] pit irq ok ก่อน shell ready.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** ลบ PIT init ใน local copyแล้วอธิบายว่า gate ควร failตรงไหน.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 2 — Serial shell

**Prediction:** ทำนายเส้นทาง input ใน -display none.

**Action:**
```text
make qemu แล้วพิมพ์ help/ticks
```

**Expected key evidence:** COM1 receive → shell_feed_char; outputกลับ COM1.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** เทียบกับ PS/2 scancode path.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.

## Example 3 — Page-fault diagnostics

**Prediction:** อธิบายข้อมูลที่ panic ต้องมี.

**Action:**
```text
inspect exception_pf_stub + exception_panic
```

**Expected key evidence:** vector/error/RIP และ CR2 สำหรับ #PF ถูกพิมพ์ก่อน halt.

**What may vary:** address, symbol placement, compiler version, formatting หรือ environment metadata.

**Explain:** เชื่อม output กลับไปยัง contract/algorithm ใน Theory และระบุสิ่งที่ evidence นี้ยังพิสูจน์ไม่ได้.

**Modification:** อธิบายเหตุผลที่ default unknown ISR ยังไม่ใช่ robust frameworkเต็ม.

**Debug rule:** ถ้าผลผิดจาก prediction ให้หา representation/contract แรกที่ต่าง ไม่แก้หลายจุดพร้อมกัน.


# Worked Examples — Final Capstone

Capstone baselineพิสูจน์ integration; assignmentบังคับให้ผู้เรียนสร้าง/แก้ของเอง.

## Example 1 — Final audit + artifact provenance

**Goal:** สร้าง evidence packageที่ย้อนกลับได้.

**Command / action:**

```bash
make -C 18-capstone clean test

cat 18-capstone/build/audit-summary.json
cat 18-capstone/build/manifest.json

sha256sum 18-capstone/build/capstone-app \
          18-capstone/build/eliteos64-kernel.elf
```

**Prediction:** hashesที่คำนวณเองต้องตรง manifest entries.

**Expected key evidence:** summary status passed; qemu_runtimeเป็น `passed` หรือ `skipped`พร้อมเหตุผล; artifactsมี SHA-256+size.

**What may vary:** hashesตาม compiler/version/source commit; นี่คือเหตุผลที่ต้อง record provenance.

**Explain:** hashระบุ exact artifactแต่ไม่พิสูจน์ security/authenticityถ้าไม่มี trusted provenance/signature.

**Modification:** rebuildด้วย Clangแล้ว compare hash/behavior.

**Failure mode:** อย่า compare hashข้าม toolchainแล้วสรุป semanticsต่างทันที.

**Reflection:** reproducible evidence packageควรเก็บ commit/tool versions/commandsอะไรบ้าง?

---

## Example 2 — Require OS runtime proof

**Goal:** แยก capstoneที่ไม่มี VM toolingจาก environmentที่ต้องพิสูจน์ QEMU runtime.

**Command / action:**

```bash
CAPSTONE_REQUIRE_QEMU=1 make -C 18-capstone clean test
cat 18-capstone/build/qemu-serial.log
```

**Prediction:** commandต้อง failถ้า QEMU/GRUB/xorrisoขาด; ถ้ามีครบต้อง boot, PIT tick และ execute serial `ticks` command.

**Expected key evidence:** logมี:
- `[BOOT] pit irq ok`
- `[BOOT] shell ready`
- `ticks=`
- promptกลับมา

**What may vary:** tick value, frame addresses.

**Explain:** static ELF/Multiboot validationไม่แทน runtime interrupt/input proof.

**Modification:** ใช้ normal `make test` ใน environmentไม่มี QEMUแล้วดู `qemu_runtime.status=skipped`.

**Failure mode:** skippedต้องไม่ถูก reportเป็น passed.

**Reflection:** อธิบาย validation pyramid static→unit→integration→VM→hardware.

---

## Example 3 — Blind RE ก่อนเปิด source

**Goal:** ใช้ artifactจาก capstoneเป็น authorized unknown binary.

**Command / action:**

```bash
file 18-capstone/build/capstone-app
readelf -hSWl 18-capstone/build/capstone-app
python3 16-reverse-engineering/projects/cfg-extract/cfg_extract.py \
  18-capstone/build/capstone-app
objdump -d -Mintel 18-capstone/build/capstone-app \
  > /tmp/capstone.dis
```

**Prediction:** หา function/CFG/callsได้บางส่วนแต่ source names/types/commentsอาจ recoverไม่ได้ครบ.

**Expected key evidence:** factsจาก ELF/disassemblyถูกแยกจาก inferenceใน report.

**What may vary:** PIE addresses/layout.

**Explain:** reverse engineeringคือ pipelineย้อนกลับแบบ loss of information.

**Modification:** เขียน pseudocodeก่อนเปิด `examples/capstone.el`; จากนั้น compareและบันทึก assumptionsผิด.

**Failure mode:** อย่าใช้ sourceเป็น “เฉลย”ก่อน blind reportเสร็จ.

**Reflection:** ให้ confidence High/Medium/Lowกับ 5 claimsพร้อม evidence.

---

## Example 4 — Learner-created deliverables

**Goal:** พิสูจน์ความสามารถสร้าง/แก้ ไม่ใช่แค่รัน solution.

**Command / action:**

```bash
sed -n '1,260p' 18-capstone/ASSIGNMENT.md
find 18-capstone/starter -maxdepth 2 -type f -print
```

**Prediction:** assignmentต้องมี compiler patch, OS patch+QEMU evidence, blind RE, defensive bug fixและ engineering defense.

**Expected key evidence:** submission treeมี design, patch, tests/logs, hashesและreports.

**What may vary:** featureที่ผู้เรียนเลือก.

**Explain:** automated baselineตรวจ repository regressions; masteryต้องมี novel modification + debugging explanation.

**Modification:** ก่อนเริ่มงานเขียน acceptance criteria/test planของ deliverableแต่ละชิ้น.

**Failure mode:** formatting/comment-only patchไม่นับ implementation; OS deliverableไม่มี QEMU evidenceไม่ผ่าน.

**Reflection:** ใช้ RUBRICให้คะแนนตัวเองแล้วระบุ 2 weak areasที่ต้อง retest.

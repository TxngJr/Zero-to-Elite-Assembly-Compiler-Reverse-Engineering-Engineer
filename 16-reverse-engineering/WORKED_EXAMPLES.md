# Worked Examples — Reverse Engineering

ใช้เฉพาะ course-owned/authorized binaries. ทุก claimให้แยก **Fact / Inference / Unknown**.

## Example 1 — O0 vs O2 โดยใช้ artifactจริง

**Goal:** เห็น compiler transformationsโดยไม่อ้างว่า source↔assembly 1:1.

**Command / action:**

```bash
make -C 16-reverse-engineering clean build-challenges

file 16-reverse-engineering/build/challenges/control-o0 \
     16-reverse-engineering/build/challenges/control-o2

objdump -d -Mintel 16-reverse-engineering/build/challenges/control-o0 \
  > 16-reverse-engineering/build/control-o0.dis
objdump -d -Mintel 16-reverse-engineering/build/challenges/control-o2 \
  > 16-reverse-engineering/build/control-o2.dis

wc -l 16-reverse-engineering/build/control-o0.dis \
      16-reverse-engineering/build/control-o2.dis
```

**Prediction:** O0มี stack-local/source-like control flowมากกว่า; O2อาจ inline/fold/reorder.

**Expected key evidence:** disassembly shapeต่าง แต่:

```bash
16-reverse-engineering/build/challenges/control-o0 5
16-reverse-engineering/build/challenges/control-o2 5
```

ต้องให้ behaviorเดียวกันสำหรับ inputเดียวกัน.

**What may vary:** exact instructions/address/layoutตาม GCC/Clang version.

**Explain:** optimizationเปลี่ยน representation ไม่ควรเปลี่ยน supported program semantics.

**Modification:** เลือก inputs `0,1,2,5,9` แล้ว compare outputsทุก variant.

**Failure mode:** ห้ามใช้ instruction-countอย่างเดียวตัดสินว่า compiler “ดีกว่า”.

**Reflection:** เขียน 3 factsจาก disassemblyและ 3 inferencesที่ต้องการ evidenceเพิ่ม.

---

## Example 2 — Basic-block CFG จริง

**Goal:** สร้าง leaders/branch/fallthrough edges ไม่ใช่แค่ list branch target.

**Command / action:**

```bash
python3 16-reverse-engineering/projects/cfg-extract/cfg_extract.py \
  16-reverse-engineering/build/challenges/control-o0

python3 16-reverse-engineering/projects/cfg-extract/cfg_extract.py \
  --json 16-reverse-engineering/build/challenges/control-o0 \
  > 16-reverse-engineering/build/control.cfg.json

python3 - <<'PY'
import json
p='16-reverse-engineering/build/control.cfg.json'
data=json.load(open(p))
for fn in data:
    if fn['name'] == 'main':
        print('main blocks =', len(fn['blocks']))
        for b in fn['blocks']:
            print(hex(b['start']), b['edges'])
PY
```

**Prediction:** conditional branchสร้าง target edge + fallthrough edge; unconditional jumpไม่มี implicit fallthrough edge.

**Expected key evidence:** JSONมี `blocks`, แต่ละ blockมี `start/end/instructions/edges`, และ callsแยกจาก intra-function CFG edges.

**What may vary:** block addresses/layout.

**Explain:** basic-block leaderมาจาก function entry, direct branch target และ instructionหลัง conditional transfer.

**Modification:** รันกับ `recursive-o0` แล้วแยก recursive call edgeออกจาก CFG branch edge.

**Failure mode:** indirect jumps/jump tablesยังเป็น limitationของ tool; ต้องรายงาน Unknown ไม่สร้าง edgeปลอม.

**Reflection:** ทำไม call graphกับ CFGเป็นคนละ graph?

---

## Example 3 — Stripped reconstruction

**Goal:** reconstruct behaviorก่อนเปิด source.

**Command / action:**

```bash
sha256sum 16-reverse-engineering/build/challenges/control-stripped
file 16-reverse-engineering/build/challenges/control-stripped
readelf -hW 16-reverse-engineering/build/challenges/control-stripped
readelf -SW 16-reverse-engineering/build/challenges/control-stripped
strings -a 16-reverse-engineering/build/challenges/control-stripped
objdump -d -Mintel 16-reverse-engineering/build/challenges/control-stripped \
  > 16-reverse-engineering/build/control-stripped.dis
```

**Prediction:** local symbol/debug namesหาย แต่ ELF headers, code bytes, dynamic metadataและ stringsบางส่วนยังอยู่.

**Expected key evidence:** `file`ระบุ stripped; `objdump`ยัง disassemble executable sectionsได้.

**What may vary:** dynamic symbol setตาม toolchain.

**Explain:** stripลบ metadataบางประเภท ไม่ได้ลบ machine instructions.

**Modification:** เขียน pseudocodeหนึ่ง functionโดยยังไม่เปิด `examples/control.c`; บันทึก confidenceต่อแต่ละ inference.

**Failure mode:** string presenceไม่พิสูจน์ pathถูก execute.

**Reflection:** เปิด sourceหลัง reportเสร็จ แล้วเขียน assumptionsที่ผิดอย่างน้อย 2 จุด.

---

## Example 4 — Tool failureต้องไม่กลายเป็น “PASS”

**Goal:** พิสูจน์ RE automation fail closedเมื่อ required ELF toolล้ม.

**Command / action:**

```bash
printf 'not an elf\n' > 16-reverse-engineering/build/not-elf.txt

set +e
python3 16-reverse-engineering/projects/binary-report/binary_report.py \
  16-reverse-engineering/build/not-elf.txt
status=$?
set -e
printf 'status=%d\n' "$status"
```

**Expected key evidence:** status non-zeroและ diagnosticขึ้นต้น `binary-report: error:`.

**What may vary:** readelf wording.

**Explain:** automationที่ ignore child-process return codeสร้าง false confidenceใน capstone/CI.

**Modification:** เปรียบเทียบ required `readelf` กับ optional `nm` behaviorบน stripped binary.

**Failure mode:** optional tool nonzeroควรถูกบันทึกเป็น structured status ไม่ทำ reportทั้งก้อนหายโดยไม่มีเหตุผล.

**Reflection:** tool pipelineควร fail hard/softอย่างไรตามความสำคัญของ evidence?

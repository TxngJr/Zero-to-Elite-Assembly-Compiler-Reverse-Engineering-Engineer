# Worked Examples — Compiler IR

ทำแบบ **Predict → Build/Run → Inspect → Explain → Modify**. เป้าหมายคือพิสูจน์ algorithm ไม่ใช่ grep ว่ามีคำบางคำ.

## Example 1 — Diamond CFG และ Dominators

**Goal:** คำนวณ dominator setsของ diamond CFGด้วยมือและเทียบ exact unit test.

**Prediction:**

```text
        entry
       /     \
    left     right
       \     /
        join
```

ควรได้:

```text
dom(entry) = {entry}
dom(left)  = {entry,left}
dom(right) = {entry,right}
dom(join)  = {entry,join}
```

**Command / action:**

```bash
python3 -m unittest -v 10-compiler-ir/tests/test_ir.py

python3 10-compiler-ir/projects/elite-ir/elite_ir.py \
  --dom 10-compiler-ir/examples/diamond.el
```

**Expected key evidence:** unit test `test_dominators_exact` ต้อง pass และ joinต้องไม่มี left/rightใน dominator set.

**What may vary:** generated block suffixเลขอาจต่างถ้า lowererเปลี่ยน naming; mathematical relationต้องเดิม.

**Explain:** node D dominate N เมื่อทุก pathจาก entryไป N ต้องผ่าน D. ทั้ง then/elseไม่อยู่บนทุก pathไป join.

**Modification:** เพิ่ม basic blockเดียวหลัง entryก่อน branch แล้วคำนวณ setsใหม่ก่อนรัน.

**Failure mode:** ถ้า testแค่เห็นคำ `function main` แล้วผ่าน นั่นไม่ใช่ semantic test; ต้อง assert exact sets.

**Reflection:** อธิบายความต่างระหว่าง predecessor, dominator และ immediate dominator.

---

## Example 2 — Liveness แบบ exact set

**Goal:** เห็น equation `IN = USE ∪ (OUT - DEF)` ทำงานจริง.

**Prediction:** สำหรับ block:

```text
x = a
y = x + b
return y
```

ที่ function exit:
- `OUT = {}`
- `IN = {a,b}`

**Command / action:**

```bash
python3 -m unittest -v \
  10-compiler-ir.tests.test_ir.IRTests.test_liveness_exact
```

ถ้า Python module pathจาก shellไม่ resolve ให้ใช้:

```bash
python3 10-compiler-ir/tests/test_ir.py -v
```

**Expected key evidence:** `test_liveness_exact ... ok`.

**What may vary:** orderingของ setตอน print; mathematical membershipห้ามเปลี่ยน.

**Explain:** `x` ไม่ live-in เพราะถูก defineก่อนใช้; `a` และ `b`ต้องมีค่าก่อน blockเริ่ม.

**Modification:** สร้าง successor blockที่ใช้ `x`; ทำนายว่า `x` จะกลายเป็น live-outของ predecessorหรือไม่.

**Failure mode:** อย่าใช้ testแบบ `grep out=`; algorithmผิดก็ยังพิมพ์ `out=` ได้.

**Reflection:** ทำไม livenessสำคัญต่อ register allocationและ dead-code elimination?

---

## Example 3 — Signed-i64 constant folding without float

**Goal:** พิสูจน์ optimizerรักษา integer semanticsตาม `LANGUAGE_SPEC.md`.

**Prediction:**

```text
9223372036854775807 / 3
= 3074457345618258602
```

และ `INT64_MIN / -1` ต้อง **ไม่ fold** เพราะ runtime `idiv` trap.

**Command / action:**

```bash
python3 10-compiler-ir/tests/test_ir.py -v

python3 10-compiler-ir/projects/elite-ir/elite_ir.py \
  --opt 10-compiler-ir/examples/fold.el
```

**Expected key evidence:**
- large division exact testผ่าน
- wrapping-add testผ่าน
- division-trap-not-folded testผ่าน
- optimizerไม่มี Python floating-point conversionใน integer division path

**What may vary:** IR temp names/formatting.

**Explain:** Python `int(a / b)` ผิดสำหรับ i64ใหญ่เพราะ `/`สร้าง float; implementationต้องใช้ integer-only truncation toward zero.

**Modification:** เพิ่ม cases:
- `INT64_MAX + 1 → INT64_MIN`
- `-7 / 3 → -2`
- `-7 % 3 → -1`

**Failure mode:** optimized/unoptimized executableให้ผลต่างกันคือ compiler correctness bug ไม่ใช่ “optimization difference”.

**Reflection:** เขียน invariant: optimizationต้องเปลี่ยน implementationแต่ต้องไม่เปลี่ยน observable semantics/trapsของโปรแกรมที่รองรับ.

---

## Example 4 — SSA construction

**Goal:** เห็น phi placement + variable renamingจริง ไม่ใช่แค่ phi-candidate list.

**Command / action:**

```bash
python3 10-compiler-ir/tests/test_ssa.py -v
python3 10-compiler-ir/projects/elite-ir/elite_ir.py \
  --ssa 10-compiler-ir/examples/diamond.el
```

**Expected key evidence:** join blockมี `phi` และ source variable versioned เช่น `x.0`, `x.1`, `x.2`.

**What may vary:** versionเลขตาม traversal order.

**Explain:** phiเลือก valueตาม predecessor edge; SSA invariantคือ source variable versionหนึ่งถูก defineครั้งเดียว.

**Modification:** ใช้ loop exampleและหา phiที่ loop header.

**Failure mode:** มีคำ `phi`อย่างเดียวไม่พิสูจน์ SSA; usesหลัง joinต้องชี้ versionของ phi destinationด้วย.

**Reflection:** อธิบายว่าทำไม SSAต้องถูก “destroy” หรือ lowerก่อน machine backendที่ไม่มี phi instruction.

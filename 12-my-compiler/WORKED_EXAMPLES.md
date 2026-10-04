# Worked Examples — My Compiler: EliteC

## Example 1 — One source through every compiler phase

**Goal:** ใช้ driverเดียวดู representationทุกชั้น.

**Command / action:**

```bash
mkdir -p 12-my-compiler/build

python3 12-my-compiler/projects/elitec/elitec.py \
  --emit tokens 12-my-compiler/examples/factorial.el \
  > 12-my-compiler/build/factorial.tokens

python3 12-my-compiler/projects/elitec/elitec.py \
  --emit ast 12-my-compiler/examples/factorial.el \
  > 12-my-compiler/build/factorial.ast.json

python3 12-my-compiler/projects/elitec/elitec.py \
  --emit ir 12-my-compiler/examples/factorial.el \
  > 12-my-compiler/build/factorial.ir

python3 12-my-compiler/projects/elitec/elitec.py \
  --emit asm 12-my-compiler/examples/factorial.el \
  > 12-my-compiler/build/factorial.s

python3 12-my-compiler/projects/elitec/elitec.py \
  12-my-compiler/examples/factorial.el \
  -o 12-my-compiler/build/factorial

file 12-my-compiler/build/factorial
```

**Prediction:** tokensรักษา lexical units; ASTรักษา source structure; IRเผย CFG/temps; assemblyเป็น target-specific; ELFเพิ่ม link/load metadata.

**Expected key evidence:** artifactทุกชั้นnon-emptyและ executableรัน status 0สำหรับ factorial regression.

**What may vary:** assembly temp/stack layoutและ ELF addresses.

**Explain:** phase boundaryที่ชัดทำให้ debugหา representationแรกที่ผิดได้.

**Modification:** เปลี่ยน base case factorialแล้วตามผลต่างทุก representation.

**Failure mode:** อย่า debug backendก่อนยืนยัน AST/IRถูก.

**Reflection:** แต่ละ phaseทำข้อมูลอะไร “หาย” และเพิ่มอะไร?

---

## Example 2 — Optimized vs unoptimized equivalence

**Goal:** พิสูจน์ optimizationไม่เปลี่ยน supported semantics.

**Command / action:**

```bash
python3 12-my-compiler/projects/elitec/elitec.py \
  12-my-compiler/examples/large_div.el \
  -o 12-my-compiler/build/large-div-O0

python3 12-my-compiler/projects/elitec/elitec.py \
  --opt 12-my-compiler/examples/large_div.el \
  -o 12-my-compiler/build/large-div-opt

set +e
12-my-compiler/build/large-div-O0
a=$?
12-my-compiler/build/large-div-opt
b=$?
set -e
printf 'unoptimized=%d optimized=%d\n' "$a" "$b"
test "$a" -eq "$b"
```

**Prediction:** statusesต้องตรง.

**Expected key evidence:** large signed division regressionไม่ต่างเพราะ optimizerใช้ integer-only folding.

**What may vary:** emitted assembly.

**Explain:** optimizerต้อง preserve wrap/trap/division semanticsใน `LANGUAGE_SPEC.md`.

**Modification:** เพิ่ม negative division/remainder tests.

**Failure mode:** output assembly “สั้นกว่า”ไม่ได้ทำ optimizerถูก.

**Reflection:** differential testingช่วยจับ compiler bugชนิดใด?

---

## Example 3 — Driver status vs program status

**Goal:** แยก compiler successจาก compiled program exit code.

**Command / action:**

```bash
python3 12-my-compiler/projects/elitec/elitec.py \
  --run 12-my-compiler/examples/return42.el \
  -o 12-my-compiler/build/return42
printf 'elitec status=%d\n' "$?"

set +e
python3 12-my-compiler/projects/elitec/elitec.py \
  --run --propagate-exit-code \
  12-my-compiler/examples/return42.el \
  -o 12-my-compiler/build/return42
status=$?
set -e
printf 'propagated status=%d\n' "$status"
```

**Prediction:** normal `--run` report program status 42แต่ compiler commandคืน 0; explicit propagateคืน 42.

**Expected key evidence:** compiler failureกับ program statusไม่ปนกันโดย default.

**What may vary:** executable path.

**Explain:** CI/toolchainควรแยก “compile failed” จาก “program intentionally returned nonzero”.

**Modification:** ลอง syntax/type errorและยืนยัน status 1 + diagnostic.

**Failure mode:** shell `set -e`จะหยุดเมื่อใช้ propagateกับ nonzero program;จับ statusอย่างตั้งใจ.

**Reflection:** CLI contractที่ดีช่วย scriptingอย่างไร?

---

## Example 4 — Invalid entry point / literal range

**Goal:** พิสูจน์ driverเคารพ language specก่อนถึง assembler.

**Command / action:**

```bash
for src in \
  12-my-compiler/examples/bad_main_args.el \
  12-my-compiler/examples/bad_main_return.el \
  12-my-compiler/examples/literal_overflow.el
do
  echo "=== $src ==="
  set +e
  python3 12-my-compiler/projects/elitec/elitec.py --check "$src"
  status=$?
  set -e
  echo "status=$status"
  test "$status" -ne 0
done
```

**Expected key evidence:** errorsเกิดเป็น source diagnostics ไม่มี Python traceback.

**What may vary:** exact wording.

**Explain:** frontendต้อง reject values/signaturesที่ backend/runtimeไม่มี contractรองรับ.

**Modification:** เพิ่ม negative cases wrong arity/unknown variable.

**Failure mode:** assembler/linker errorช้าเกินไปถ้า frontendรู้ violationอยู่แล้ว.

**Reflection:** เขียน checklistเมื่อต้องเพิ่ม featureภาษาใหม่หนึ่ง feature.

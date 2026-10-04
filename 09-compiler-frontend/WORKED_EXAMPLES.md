# Worked Examples — Compiler Frontend

ทำตามลำดับ **Predict → Run → Observe → Explain → Modify**. ตัวอย่างนี้ตั้งใจให้ copy/run ได้จาก root ของ repository.

## Example 1 — Precedence AST: `1 + 2 * 3`

**Goal:** พิสูจน์ว่า parser ให้ `*` bind แน่นกว่า `+`.

**Prediction:** ก่อนรันให้วาด AST:

```text
Binary(+)
├── Int(1)
└── Binary(*)
    ├── Int(2)
    └── Int(3)
```

**Command / action:**

```bash
mkdir -p 09-compiler-frontend/build
cat > 09-compiler-frontend/build/precedence.el <<'EOF'
fn main() -> int {
  return 1 + 2 * 3;
}
EOF

python3 09-compiler-frontend/projects/elite-frontend/elite_frontend.py \
  --tokens 09-compiler-frontend/build/precedence.el

python3 09-compiler-frontend/projects/elite-frontend/elite_frontend.py \
  --ast 09-compiler-frontend/build/precedence.el \
  > 09-compiler-frontend/build/precedence.ast.json
cat 09-compiler-frontend/build/precedence.ast.json
```

**Expected key evidence:**
- token stream มี `INT '1'`, `+`, `INT '2'`, `*`, `INT '3'`
- AST root expressionมี `"op": "+"`
- right childของ rootมี `"op": "*"`
- AST ไม่ควรตีความเป็น `(1 + 2) * 3`

**What may vary:** JSON indentation/field orderingอาจเปลี่ยนถ้า serializerเปลี่ยน แต่ tree semanticsต้องเดิม.

**Explain:** `parse_additive()` เรียก `parse_multiplicative()` เพื่อสร้าง operand ก่อน จึงทำให้ multiplicationอยู่ลึกกว่า addition.

**Modification:**

```bash
sed 's/1 + 2 \* 3/(1 + 2) * 3/' \
  09-compiler-frontend/build/precedence.el \
  > 09-compiler-frontend/build/precedence-paren.el

python3 09-compiler-frontend/projects/elite-frontend/elite_frontend.py \
  --ast 09-compiler-frontend/build/precedence-paren.el
```

ทำนาย AST ใหม่ก่อนรัน.

**Failure mode:** ถ้า root ยังเป็น `+` หลังใส่วงเล็บ ให้ตรวจ `parse_primary()` และลำดับ precedence functions.

**Reflection:** อธิบายด้วยภาษาตัวเองว่าทำไม precedence ไม่ได้มาจาก token แต่เกิดจาก parser structure.

---

## Example 2 — Syntax-valid แต่ type-invalid

**Goal:** แยก parser success ออกจาก semantic/type-check failure.

**Prediction:** source ด้านล่าง tokenize/parse ได้ แต่ checkerต้อง reject เพราะ `bool` รับ `int`.

**Command / action:**

```bash
cat > 09-compiler-frontend/build/type-invalid.el <<'EOF'
fn main() -> int {
  let ready: bool = 42;
  return 0;
}
EOF

set +e
python3 09-compiler-frontend/projects/elite-frontend/elite_frontend.py \
  --check 09-compiler-frontend/build/type-invalid.el
status=$?
set -e
printf 'frontend status=%d\n' "$status"
```

**Expected key evidence:**
- command exit statusต้อง non-zero
- diagnosticมีใจความประมาณ `let ready: expected bool, got int`
- ไม่ควรมี Python traceback

**What may vary:** ตำแหน่ง/wording diagnosticอาจพัฒนาได้ แต่ error classต้องยังเป็น source diagnostic.

**Explain:** grammarอนุญาต `let name: type = expression;`; type checkerต่างหากที่ตรวจว่า expression typeตรง declaration.

**Modification:** เปลี่ยนเป็น `let ready: bool = true;` แล้ว `--check` ต้องพิมพ์ `OK`.

**Failure mode:** ถ้า invalid programผ่าน checker ให้เพิ่ม regression testก่อนแก้ implementation.

**Reflection:** ยกตัวอย่าง syntax errorหนึ่งกรณีและ semantic errorหนึ่งกรณี แล้วอธิบายว่าเกิดคนละ phase.

---

## Example 3 — Entry-point ABI contract

**Goal:** พิสูจน์ว่า EliteLang v0.2 บังคับ `fn main() -> int`.

**Prediction:** `main(x:int)` และ `main()->bool` ต้องถูก reject.

**Command / action:**

```bash
cat > 09-compiler-frontend/build/bad-main.el <<'EOF'
fn main(x: int) -> int {
  return x;
}
EOF

set +e
python3 09-compiler-frontend/projects/elite-frontend/elite_frontend.py \
  --check 09-compiler-frontend/build/bad-main.el
status=$?
set -e
printf 'status=%d\n' "$status"
```

**Expected key evidence:** diagnosticระบุ `main must have signature: fn main() -> int`.

**What may vary:** byte position/formattingของ messageไม่ใช่ contract; signature requirementคือ contract.

**Explain:** host C runtimeเรียก symbol `main`ตาม ABI/runtime convention; ภาษาเราไม่ควรปล่อย arbitrary source signatureถ้าไม่มี runtime bridgeรองรับ.

**Modification:** สร้าง literal `9223372036854775808` ใน `main` แล้ว checkerต้อง reject signed-i64 range.

**Failure mode:** ถ้า literalใหญ่ผ่าน frontend แต่ backendรับไม่ได้ แสดง representation contractระหว่าง frontend/backendแตก.

**Reflection:** เปิด [../LANGUAGE_SPEC.md](../LANGUAGE_SPEC.md) แล้วสรุป 3 semantic contractsที่ frontendต้อง enforce.

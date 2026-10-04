# Worked Examples — Compiler Backend

ตัวอย่างนี้ให้ inspect assemblyจริงและเทียบกับ System V AMD64 ABI.

## Example 1 — Stack-slot frame และ alignment

**Goal:** อธิบายว่า baseline backend map virtual valuesลง stackอย่างไร.

**Command / action:**

```bash
mkdir -p 11-compiler-backend/build
python3 11-compiler-backend/projects/elite-backend/elite_backend.py \
  11-compiler-backend/examples/return42.el \
  -o 11-compiler-backend/build/return42.s

sed -n '1,120p' 11-compiler-backend/build/return42.s
```

**Prediction:** ต้องเห็น `push rbp`, `mov rbp,rsp`; frame allocationถ้ามีต้อง roundเป็น multiple of 16.

**Expected key evidence:** prologue/epilogueสมดุล และทุก stack-slot accessอยู่ที่ `[rbp-offset]`.

**What may vary:** จำนวน/temp slotsตาม IR generation.

**Explain:** SysV callerต้องมี stack alignmentที่ถูกก่อน `call`; backendใช้ frameขนาด multiple 16หลัง `push rbp`.

**Modification:** เพิ่ม localsหลายตัวใน local sourceแล้วดู frame sizeเปลี่ยน.

**Failure mode:** อย่าสรุป frameถูกเพียงเพราะ assemblerรับ; runtime calls/stack argsต้องมี testsด้วย.

**Reflection:** spill-everything correctแต่เสีย performanceอย่างไร?

---

## Example 2 — 8 arguments: registers + stack

**Goal:** พิสูจน์ boundaryของ first-six integer arguments.

**Command / action:**

```bash
python3 12-my-compiler/projects/elitec/elitec.py \
  --emit asm 12-my-compiler/examples/sum8.el \
  > 11-compiler-backend/build/sum8.s

grep -n -E 'call|push|rdi|rsi|rdx|rcx|r8|r9|\[rbp\+' \
  11-compiler-backend/build/sum8.s
```

**Prediction:**
- args 1–6: RDI, RSI, RDX, RCX, R8, R9
- args 7–8: caller stack
- calleeอ่าน stack argsหลัง saved RBP/return address

**Expected key evidence:** caller push stack arguments in reverse order; calleeใช้ positive `rbp` offsets; cleanupเกิดหลัง call.

**What may vary:** temp loads/stack slotsรอบ argument setup.

**Explain:** stack alignmentต้องยังถูกเมื่อจำนวน stack argsเป็น odd; baseline backendจึงอาจเพิ่ม padding 8 bytes.

**Modification:** สร้าง 7-argและ9-arg functionแล้วตรวจ padding.

**Failure mode:** โปรแกรม 6 argsผ่านไม่ได้พิสูจน์ stack-argument path.

**Reflection:** วาด stackก่อน call, หลัง call, หลัง callee `push rbp`.

---

## Example 3 — Signed division / remainder

**Goal:** ผูก language semanticsกับ x86 `idiv`.

**Command / action:**

```bash
cat > 11-compiler-backend/build/div.el <<'EOF'
fn main() -> int {
  if (((-7 / 3) == -2) && ((-7 % 3) == -1)) {
    return 0;
  } else {
    return 1;
  }
}
EOF

python3 12-my-compiler/projects/elitec/elitec.py \
  --emit asm 11-compiler-backend/build/div.el \
  > 11-compiler-backend/build/div.s

grep -n -E 'cqo|idiv|rdx|rax' 11-compiler-backend/build/div.s
```

**Expected key evidence:** signed division pathใช้ `cqo`ก่อน `idiv`; quotientอยู่ RAX, remainderอยู่ RDX.

**What may vary:** stack-slot offsets.

**Explain:** `cqo` sign-extends RAX into RDX:RAX. EliteLang quotient truncates toward zeroตรงกับ `idiv`.

**Modification:** ลอง divisor 0ใน isolated processและอธิบายว่าทำไม optimizerห้าม fold trapออก.

**Failure mode:** อย่ารัน trap caseเป็นส่วนของ shell scriptภายใต้ `set -e` โดยไม่ isolate/จับ status.

**Reflection:** `INT64_MIN / -1` มีอะไรพิเศษ?

---

## Example 4 — Linear-scan allocation lab

**Goal:** แยก “allocator algorithm lab” ออกจาก baseline codegenที่ยัง spillทุก value.

**Command / action:**

```bash
python3 11-compiler-backend/tests/test_linear_scan.py -v
python3 11-compiler-backend/projects/linear-scan/linear_scan.py
```

**Expected key evidence:** non-overlapping intervals reuse register; overlapping intervalsแยก register; pressureทำให้มี spill.

**What may vary:** register namesถ้า input poolเปลี่ยน.

**Explain:** interval start/endมาจาก liveness approximation; linear scanเลือก registerด้วย active intervalsและ spill policy.

**Modification:** เปลี่ยน register poolเหลือหนึ่งตัวและทำนายว่า intervalใด spill.

**Failure mode:** การมี allocator labไม่ได้หมายความว่า EliteC production backendใช้ allocatorแล้ว.

**Reflection:** ระบุขั้น integrationที่ต้องทำเพื่อให้ codegen consume allocation resultจริง.

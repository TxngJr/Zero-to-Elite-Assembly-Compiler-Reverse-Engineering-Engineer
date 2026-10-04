# Worked Examples — x86-64 Assembly

เน้น bytes/registers/flags/effective addressด้วย evidenceจาก assemblerและ GDB.

## Example 1 — 32-bit register write zero-extends

**Goal:** เข้าใจ RAX/EAX/AX/AL semantics.

**Command / action:**

```bash
cat >/tmp/regwrite.s <<'EOF'
.intel_syntax noprefix
.global main
main:
    mov rax, -1
    mov eax, 5
    ret
EOF

gcc -g -no-pie /tmp/regwrite.s -o /tmp/regwrite
gdb -q /tmp/regwrite
```

ใน GDB:

```text
break main
run
si
si
info registers rax eax
quit
```

**Prediction:** หลัง `mov eax,5`, RAX = `0x0000000000000005`.

**Expected key evidence:** upper 32 bitsถูก zeroโดย architecture rule.

**What may vary:** instruction addresses.

**Explain:** write EAXมี special zero-extension; write AX/ALไม่ zero upper bits.

**Modification:** เปลี่ยน `mov eax,5` เป็น `mov ax,5` แล้วทำนาย RAX.

**Failure mode:** อย่าเหมารวม partial-register semanticsทุก width.

**Reflection:** ทำไม compilerชอบ `xor eax,eax`/32-bit writesเมื่อสร้าง zero?

---

## Example 2 — Effective address vs memory load

**Goal:** แยก LEAจาก dereference.

**Command / action:**

```bash
gcc -c 03-x86-64-assembly/examples/addressing.s \
  -o /tmp/addressing.o
objdump -dr -Mintel /tmp/addressing.o
```

**Prediction:** `lea rax,[rdi+rdi*2]` คำนวณ `3*rdi` โดยไม่อ่าน memory.

**Expected key evidence:** LEA operand syntaxดูเหมือน memory addressingแต่ instructionไม่ load bytesจาก addressนั้น.

**What may vary:** assembler encoding/address offsets.

**Explain:** effective address formula = base + index*scale + displacement; scaleเป็น 1/2/4/8.

**Modification:** คำนวณ `[rax+rcx*8+16]` เมื่อ RAX=0x1000, RCX=3 → 0x1028.

**Failure mode:** อย่าใส่ arbitrary scaleเช่น 3ใน x86 addressing encoding.

**Reflection:** array int32/int64ควรใช้ scaleใด?

---

## Example 3 — CMP/Jcc signed vs unsigned

**Goal:** เห็น flagsเดียวกันตีความต่างตาม Jcc.

**Command / action:**

```bash
gcc -c 03-x86-64-assembly/examples/branches.s -o /tmp/branches.o
objdump -dr -Mintel /tmp/branches.o
```

**Prediction:** signed relationใช้ `jl/jle/jg/jge`; unsignedใช้ `jb/jbe/ja/jae`.

**Expected key evidence:** `cmp`ไม่เก็บ subtraction resultแต่ update flags; branchเลือก conditionจาก flags.

**What may vary:** labels/address.

**Explain:** CFเกี่ยวกับ unsigned borrow/carry; SF/OF relationเกี่ยวกับ signed comparison.

**Modification:** เลือก bytes `0xFF`กับ `0x01`; ตีความ signed/unsignedแล้วทำนาย branchสองแบบ.

**Failure mode:** ใช้ `jl`กับ unsigned lengthอาจผิดกรณี high bit set.

**Reflection:** เขียน bugตัวอย่างที่ signednessผิดแล้วสร้าง security/logic issueได้โดยไม่ต้อง exploit.

---

## Example 4 — Assembly + C ABI project

**Goal:** เชื่อม hand-written assemblyกับ C test harness.

**Command / action:**

```bash
make -C 03-x86-64-assembly/projects/array-kernels clean test
objdump -d -Mintel \
  03-x86-64-assembly/projects/array-kernels/array-kernels \
  | less
```

ถ้า binaryชื่อแตกต่าง ให้ดู Makefileแล้ว inspect artifactที่สร้าง.

**Prediction:** function argsมาตาม SysV ABIและ loopใช้ element strideตรงชนิดข้อมูล.

**Expected key evidence:** C testsยืนยัน semantics; disassemblyยืนยัน register/memory pattern.

**What may vary:** link addresses.

**Explain:** test behaviorกับ disassembly evidenceต้องใช้คู่กัน.

**Modification:** เพิ่ม empty array / one-element caseใน local tests.

**Failure mode:** assembly linkได้ไม่ได้แปลว่า ABIถูก.

**Reflection:** ก่อน reverse functionหนึ่งตัว ให้เขียน checklist register args, return, stack, memory width, signedness, calls, branches.

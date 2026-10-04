# Worked Examples — ABI & Linux Syscalls

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — Eight integer arguments

**Goal:** Eight integer arguments

**Prediction:** ทำนายตำแหน่ง arg1..arg8

**Command / action:**

```text
inspect abi-lab disassembly/GDB
```

**Expected key evidence:** 1–6: RDI RSI RDX RCX R8 R9; 7+ บน stack.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปลี่ยน arg count เป็น 6/7/8 แล้ววาด stack.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Stack alignment

**Goal:** Stack alignment

**Prediction:** คำนวณ RSP mod 16 ก่อน call

**Command / action:**

```text
break before call; p/x $rsp
```

**Expected key evidence:** caller ต้องจัด alignment ตาม SysV contract.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เพิ่ม push หนึ่งครั้งแล้วหาวิธี restore alignment.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — Raw write syscall

**Goal:** Raw write syscall

**Prediction:** ตาม syscall number/args โดยไม่ใช้ libc

**Command / action:**

```text
run syscall example under strace
```

**Expected key evidence:** write syscall เห็น fd/buffer/count และ return.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปลี่ยน fd เป็น stderr แล้วสังเกต.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


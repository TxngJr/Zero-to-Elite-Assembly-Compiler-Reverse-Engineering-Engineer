# Worked Examples — Debugging Engineering

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — Breakpoint and call stack

**Goal:** Breakpoint and call stack

**Prediction:** ทำนาย stack frames ก่อน break

**Command / action:**

```text
gdb: break, run, bt
```

**Expected key evidence:** backtrace แสดง active call chain.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** break callee ต่างจุดแล้วเปรียบเทียบ.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Watchpoint

**Goal:** Watchpoint

**Prediction:** หาว่าใครเปลี่ยน variable/memory

**Command / action:**

```text
watch expression; continue
```

**Expected key evidence:** GDB หยุดที่ write ที่เปลี่ยนค่า.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** ใช้ hardware watchpointกับ array element.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — Crash triage

**Goal:** Crash triage

**Prediction:** แยก crash site/root cause

**Command / action:**

```text
run crashing course binary in GDB
```

**Expected key evidence:** signal/RIP/backtrace เป็น evidence เริ่มต้น.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** inspect input/state ก่อน instruction ที่พัง.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


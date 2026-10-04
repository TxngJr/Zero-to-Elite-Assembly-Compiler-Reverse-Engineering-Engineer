# Worked Examples — Debugging Engineering

## Example 1 — Breakpoint, stack, registers

**Goal:** ใช้ GDBเพื่อพิสูจน์ call state ไม่ใช่เดาจาก source.

**Command / action:**

```bash
gcc -O0 -g -Wall -Wextra \
  08-debugging/examples/debug_target.c \
  -o /tmp/debug_target

gdb -q /tmp/debug_target
```

ใน GDB:

```text
break main
run
break helper
continue
bt
info args
info locals
info registers
disassemble /r helper
si
ni
quit
```

**Prediction:** backtraceแสดง caller→callee; argsสอดคล้อง ABI/Debug info.

**Expected key evidence:** breakpointหยุดก่อน/ใน target; registers/memoryเปลี่ยนตาม instructions.

**What may vary:** addresses/register allocationถ้า compiler/flagsเปลี่ยน.

**Explain:** source stepping (`next/step`) กับ instruction stepping (`ni/si`)ตอบคนละระดับ representation.

**Modification:** compile `-O2 -g` แล้วลองคำสั่งเดิม.

**Failure mode:** optimized buildอาจ inline/omit locals; นี่ไม่ใช่ GDB bugเสมอ.

**Reflection:** เมื่อ source lineกับ instructionsไม่ 1:1 คุณจะเลือก evidenceอะไร?

---

## Example 2 — Crash root causeด้วย sanitizer + GDB

**Goal:** ไม่หยุดที่ “โปรแกรม segfault”.

**Command / action:**

```bash
gcc -O1 -g -fno-omit-frame-pointer \
  -fsanitize=address,undefined \
  08-debugging/examples/crash_target.c \
  -o /tmp/crash_target

set +e
/tmp/crash_target
status=$?
set -e
printf 'status=%d\n' "$status"
```

**Prediction:** sanitizerให้ defect class + stack frameใกล้ invalid operation.

**Expected key evidence:** project source locationและaccess type/size.

**What may vary:** addresses/allocator details.

**Explain:** crash siteอาจช้ากว่า corruption; sanitizer instrumentationช่วย detectตอน invariantแตก.

**Modification:** ทำ fixed local copyและเพิ่ม regression input.

**Failure mode:** อย่าแค่ catch/ignore signalเพื่อให้ programจบ 0.

**Reflection:** ระบุ symptom, crash site, root causeเป็นสามบรรทัดแยกกัน.

---

## Example 3 — Watchpointกับ state corruption

**Goal:** หา “ใครเขียนค่านี้” แทนการไล่ printทุก function.

**Command / action:**

```bash
make -C 08-debugging/projects/debug-lab clean all
gdb -q 08-debugging/projects/debug-lab/debug-lab
```

ชื่อ binaryอาจต่างตาม Makefile; ใช้ artifactที่ projectสร้าง.

ใน GDB:
```text
break main
run
# หา address/variable ของ quantity/count ที่ labให้ตรวจ
watch variable_name
continue
bt
disassemble /m
```

**Prediction:** watchpointหยุดตอน writeที่เปลี่ยน monitored storage.

**Expected key evidence:** PC/backtraceชี้ writerไม่ใช่จุดที่ valueถูกอ่านผิดภายหลัง.

**What may vary:** hardware watchpoint availabilityและ optimized locals.

**Explain:** watchpoint monitor memory/register expressionตาม debugger capability.

**Modification:** ใช้ conditional breakpointแทนแล้ว compareความเหมาะสม.

**Failure mode:** watch huge/changing expressionอาจช้า/unsupported.

**Reflection:** breakpoint, watchpoint, assertion, sanitizerเลือกใช้เมื่อไร?

---

## Example 4 — O0 vs O2 debugging

**Goal:** ปรับ mental modelเมื่อ optimizerเปลี่ยน code shape.

**Command / action:**

```bash
gcc -O0 -g 08-debugging/examples/optimized.c -o /tmp/optimized-O0
gcc -O2 -g 08-debugging/examples/optimized.c -o /tmp/optimized-O2

objdump -d -Mintel /tmp/optimized-O0 > /tmp/O0.dis
objdump -d -Mintel /tmp/optimized-O2 > /tmp/O2.dis
diff -u /tmp/O0.dis /tmp/O2.dis || true
```

**Prediction:** O2อาจ inline/fold/eliminate source locals.

**Expected key evidence:** both executable behaviorเหมือนใน supported inputsแต่ debug steppingต่าง.

**What may vary:** exact optimizations.

**Explain:** debuggerแสดง reconstructed source viewจาก DWARF + machine state; optimized codeไม่ได้ preserveทุก source variable/location.

**Modification:** ใช้ `disassemble /r` และ register evidenceแก้โจทย์หนึ่งโดยไม่พึ่ง `print local`.

**Failure mode:** อย่า compile production issueด้วย O0แล้วสมมติ bug behaviorเหมือน O2ถ้า UB/race involved.

**Reflection:** ทำไม low-level debuggingต้องเข้าใจ compiler?

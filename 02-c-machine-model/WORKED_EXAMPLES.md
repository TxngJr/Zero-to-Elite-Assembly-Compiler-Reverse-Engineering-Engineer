# Worked Examples — C Machine Model

บทนี้ดู C ผ่าน object, bytes, addresses, lifetime และ compiler output.

## Example 1 — Array ไม่ใช่ pointer

**Goal:** แยก array objectจาก pointer value.

**Command / action:**

```bash
gcc -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g \
  02-c-machine-model/examples/arrays.c \
  -o /tmp/c-arrays
/tmp/c-arrays
```

**Prediction:** ใน scopeที่ arrayยังเป็น array, `sizeof array` เท่าจำนวน bytesทั้ง object; pointerมี `sizeof pointer` ตาม machine ABI.

**Expected key evidence:** addressของ first elementสัมพันธ์กับ array base แต่ `sizeof`แสดงว่า arrayกับ pointerไม่ใช่ objectเดียวกัน.

**What may vary:** addressและ pointer sizeบน non-course architecture; course target x86-64มัก 8 bytes.

**Explain:** array-to-pointer conversionเกิดในหลาย expression contexts แต่ไม่เปลี่ยน declarationของ arrayให้เป็น pointer.

**Modification:** สร้าง `int a[10]`; ทำนาย `sizeof a`, `sizeof &a`, `sizeof a[0]`.

**Failure mode:** อย่าใช้ `sizeof(pointer) / sizeof(pointer[0])` หา dynamic array length.

**Reflection:** อธิบาย `a+1` กับ `&a+1` ต่างกันอย่างไร.

---

## Example 2 — Struct padding / offsetof

**Goal:** เห็น layoutเป็น ABI/compiler decisionที่ตรวจได้.

**Command / action:**

```bash
gcc -std=c17 -Wall -Wextra -Wpedantic -g \
  02-c-machine-model/examples/struct_layout.c \
  -o /tmp/struct_layout
/tmp/struct_layout
```

**Prediction:** field offsetsอาจมี gapsเพื่อ alignment; `sizeof(struct)` อาจมากกว่าผลรวม field sizes.

**Expected key evidence:** outputแสดง offsets/alignment/paddingที่สอดคล้องกับ x86-64 ABI.

**What may vary:** layoutบน architecture/ABIอื่น.

**Explain:** compilerต้องจัดแต่ละ memberตาม alignment constraintและทำ tail paddingเพื่อ array-of-struct alignment.

**Modification:** reorder fieldsใน local copyแล้ว compare `sizeof`.

**Failure mode:** ห้าม serialize raw structแล้วถือว่า portable file/network format.

**Reflection:** ทำไม `offsetof` ดีกว่าการเดา offsetจาก field sizes?

---

## Example 3 — Sanitizer หา bounds bug

**Goal:** แยก undefined behaviorจาก “โปรแกรมเหมือนยังรันได้”.

**Command / action:**

```bash
gcc -std=c17 -Wall -Wextra -Wpedantic -g -O1 \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  02-c-machine-model/examples/buggy_bounds.c \
  -o /tmp/buggy_bounds

set +e
/tmp/buggy_bounds
status=$?
set -e
printf 'status=%d\n' "$status"
```

**Prediction:** sanitizerควร report out-of-bounds/related invalid access.

**Expected key evidence:** non-zero statusหรือ sanitizer diagnosticที่ชี้ first invalid project access.

**What may vary:** exact stack addresses/diagnostic formatting.

**Explain:** UBหมายถึงภาษา Cไม่กำหนด behavior; “ยังไม่ crash”ไม่ได้ทำให้ accessถูก.

**Modification:** แก้ loop boundใน local copyแล้วรัน sanitizerใหม่.

**Failure mode:** อย่าปิด sanitizerเพื่อให้ testเขียว; แก้ invariant.

**Reflection:** crash siteกับ root causeอาจต่างกันอย่างไร?

---

## Example 4 — Optimization ทำให้ source variableหาย

**Goal:** เห็นว่า compiler observationไม่ใช่ language guarantee.

**Command / action:**

```bash
gcc -std=c17 -O0 -g -S \
  02-c-machine-model/examples/optimization.c -o /tmp/opt-O0.s

gcc -std=c17 -O2 -g -S \
  02-c-machine-model/examples/optimization.c -o /tmp/opt-O2.s

diff -u /tmp/opt-O0.s /tmp/opt-O2.s || true
```

**Prediction:** O2อาจ fold constants, eliminate locals หรือ inline.

**Expected key evidence:** assemblyไม่ map source 1:1.

**What may vary:** optimization choicesตาม compiler/version.

**Explain:** C abstract machineกำหนด observable semantics; compilerมีอิสระ transformตราบใดที่ preserve semanticsภายใต้ language rules.

**Modification:** เพิ่ม `volatile`ใน local experimentแล้วดู codegenต่าง—but explainว่ามันไม่ใช่ thread synchronization.

**Failure mode:** อย่าสรุปว่า variable “อยู่ stackเสมอ”.

**Reflection:** บอก 3 เหตุผลที่ GDBอาจแสดง `<optimized out>`.

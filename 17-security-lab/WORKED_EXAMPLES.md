# Worked Examples — Defensive Security Lab

ใช้เฉพาะ course-owned code. เป้าหมายคือ **detect → root cause → fix → regression**, ไม่ใช่ exploit development.

## Example 1 — Length-prefixed parser bounds

**Goal:** หา invariantที่ต้องตรวจ **ก่อน** copy.

**Command / action:**

```bash
make -C 17-security-lab/projects/parser-lab clean test
make -C 17-security-lab/projects/parser-lab sanitizer-demo
```

**Prediction:** fixed testsผ่าน; injected buildต้องถูก ASanจับ.

**Expected key evidence:** sanitizer reportระบุ memory errorใน course parser path และ command injected-demoถือว่า “สำเร็จ”ก็ต่อเมื่อ sanitizer detect defect.

**What may vary:** addresses/stack frame formatting.

**Explain:** ต้องตรวจทั้ง:
- `claimed <= input_remaining`
- `claimed <= PAYLOAD_MAX`

ก่อน `memcpy`.

**Modification:** เพิ่ม regression cases `claimed=0`, `PAYLOAD_MAX`, `PAYLOAD_MAX+1`.

**Failure mode:** crash siteภายหลังไม่จำเป็นต้องเป็น corruption root cause; ใช้ first invalid project access.

**Reflection:** ทำไม stack protector/NXไม่แทน bounds check?

---

## Example 2 — Lifetime + format-string defenses

**Goal:** แยก runtime lifetime bugกับ compile-time unsafe API usage.

**Command / action:**

```bash
make -C 17-security-lab/projects/lifetime-lab clean test
make -C 17-security-lab/projects/lifetime-lab sanitize-demo

make -C 17-security-lab/projects/format-lab clean test
make -C 17-security-lab/projects/format-lab unsafe-check
```

**Prediction:**
- normal lifetime implementationผ่าน
- injected UAFถูก ASanจับ
- injected non-literal formatถูก `-Werror=format-security` ปฏิเสธ

**Expected key evidence:** logsมี AddressSanitizer/use-after-freeสำหรับ injected lifetime build; format unsafe build compileไม่ผ่าน.

**What may vary:** compiler diagnostic wording.

**Explain:** UAFแก้ที่ ownership/lifetime; การ set aliasหนึ่งตัวเป็น NULLไม่แก้ aliasesอื่น. Format misuseแก้ด้วย literal format เช่น `printf("%s", text)`.

**Modification:** วาด ownership graphก่อน/หลัง free.

**Failure mode:** อย่าเปลี่ยน testให้ “ไม่ crash”ด้วยการซ่อน sanitizer report; patch invariantแทน.

**Reflection:** compile-time defenseกับ runtime instrumentationครอบ bug classesต่างกันอย่างไร?

---

## Example 3 — Data race + TSan

**Goal:** เห็น raceเป็น invariant/concurrency problem ไม่ใช่แค่ “ผลบางครั้งผิด”.

**Command / action:**

```bash
make -C 17-security-lab/projects/race-lab clean test

# optional diagnostic environmentที่รองรับ ThreadSanitizer:
make -C 17-security-lab/projects/race-lab tsan-demo
```

**Prediction:** synchronized default pathให้ `counter=40000`; injected raceต้องถูก TSan reportเมื่อ runtimeรองรับ.

**Expected key evidence:** default deterministic testผ่าน; TSan injected pathมี `data race`/ThreadSanitizer diagnostic.

**What may vary:** TSan availability/platform support และ exact interleaving.

**Explain:** `volatile`ไม่สร้าง mutual exclusionหรือ happens-before relation.

**Modification:** อธิบาย alternative fixด้วย atomic counterกับ mutexและ trade-off.

**Failure mode:** raceอาจ “ดูถูก”หลายครั้งโดยยังมี data race; outputถูกครั้งเดียวไม่ใช่ proof.

**Reflection:** sanitizerสะอาดหนึ่ง runพิสูจน์ absenceของ racesหรือไม่?

---

## Example 4 — Random smoke vs coverage-guided fuzzing

**Goal:** ไม่เรียก pseudo-random loopว่า coverage-guided fuzzing.

**Command / action:**

```bash
make -C 17-security-lab/projects/fuzz-lab clean test

# requires clang/libFuzzer runtime
make -C 17-security-lab/projects/fuzz-lab libfuzzer CLANG=clang
```

**Prediction:** first commandรัน deterministic 5000-case smoke; secondใช้ libFuzzer corpus + instrumentation.

**Expected key evidence:** libFuzzer outputมี corpus/coverage-style progressและ `-runs=2000`; no crashไม่ใช่ security proof.

**What may vary:** coverage counters/corpus growthตาม compiler version.

**Explain:** seed corpusช่วยเข้าถึง structured parser states; coverage feedbackต่างจากสุ่ม bytesเฉย ๆ.

**Modification:** เพิ่ม valid boundary seedและเก็บ discovered failureเป็น regression inputถ้ามี.

**Failure mode:** ลบ crash artifactเพื่อให้ CIเขียวโดยไม่ root-causeถือว่าแก้ผิด.

**Reflection:** เขียน chain: fuzz finding → minimize → reproduce → root cause → patch → regression → rerun fuzz.

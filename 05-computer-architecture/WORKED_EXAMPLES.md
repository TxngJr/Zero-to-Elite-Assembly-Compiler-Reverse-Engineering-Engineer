# Worked Examples — Computer Architecture

Labsบทนี้สร้าง modelที่วัดได้ ไม่อ้างว่า simulatorเท่ากับ CPUจริง.

## Example 1 — Spatial locality

**Goal:** เชื่อม access patternกับ cache behavior.

**Command / action:**

```bash
gcc -O2 -std=c17 -Wall -Wextra -Wpedantic \
  05-computer-architecture/examples/locality.c \
  -o /tmp/locality
/tmp/locality
```

**Prediction:** sequential traversalมัก cache-friendlyกว่า large-stride/random pattern.

**Expected key evidence:** timing/operation patternสะท้อน locality แต่ absolute timeไม่ใช่ invariant.

**What may vary:** CPU, cache size, scheduler, turbo, VM noise.

**Explain:** cache lineดึง bytesเป็นกลุ่ม; spatial localityใช้ bytesใกล้กันก่อน eviction.

**Modification:** เปลี่ยน stride 1/4/16/64และ plot/จดเวลาแบบหลายรอบ.

**Failure mode:** benchmarkครั้งเดียวพิสูจน์ microarchitectureไม่ได้.

**Reflection:** แยก cache capacity, line size, associativity effects.

---

## Example 2 — Direct-mapped cache simulator

**Goal:** เห็น tag/index/offsetและ conflict miss.

**Command / action:**

```bash
make -C 05-computer-architecture/projects/cache-sim clean test
05-computer-architecture/projects/cache-sim/cache-sim
```

ถ้า binaryชื่อแตกต่าง ให้ดู Makefile.

**Prediction:** addressesที่ map indexเดียวแต่ tagต่างจะ evictกันใน direct-mapped model.

**Expected key evidence:** hit/miss countersเปลี่ยนตาม sequenceที่กำหนด.

**What may vary:** noneถ้า simulator deterministic.

**Explain:** address splitเป็น block offset + set/index + tagตาม model parameters.

**Modification:** สร้าง sequence A,B,A ที่ A/B conflict indexเดียวแล้วทำนาย misses.

**Failure mode:** อย่าเอา simulator direct-mappedไปอ้างว่า L1 ของ CPUคุณมี designเดียวกัน.

**Reflection:** set associativityช่วย conflictอย่างไร?

---

## Example 3 — Branch predictor simulator

**Goal:** เข้าใจ predictor stateโดยไม่พึ่ง perf countersก่อน.

**Command / action:**

```bash
make -C 05-computer-architecture/projects/branch-predictor clean test
05-computer-architecture/projects/branch-predictor/branch-predictor
```

**Prediction:** repeating patternกับ alternating patternให้ accuracyต่างตาม predictor algorithm.

**Expected key evidence:** deterministic prediction/misprediction counts.

**What may vary:** noneใน simulator; real hardwareซับซ้อนกว่ามาก.

**Explain:** mispredictionทำให้ speculative workถูก squashและ frontendต้อง redirect.

**Modification:** feed pattern `TTTTNNNN`, `TNTN...`, loop-like `TTTTTTTN`.

**Failure mode:** simulator simple predictorไม่ใช่ reverse-engineered predictorของ CPUจริง.

**Reflection:** ทำไม branchless codeไม่ได้เร็วกว่าเสมอ?

---

## Example 4 — Tiny CPU fetch/decode/execute

**Goal:** เชื่อม ISA stateกับ execution loop.

**Command / action:**

```bash
make -C 05-computer-architecture/projects/tiny-cpu clean test
05-computer-architecture/projects/tiny-cpu/tiny-cpu
```

**Prediction:** trace PC/registersทีละ instructionก่อนดู output.

**Expected key evidence:** PCเลือก instructionถัดไป, decodeเลือก operation, executeเปลี่ยน architectural state.

**What may vary:** trace formatting.

**Explain:** simulatorเป็น architectural model; real CPUอาจ pipeline/out-of-orderแต่ต้อง retireผลให้สอดคล้อง ISA.

**Modification:** เพิ่ม programเล็กที่ loop 3 รอบโดยไม่เพิ่ม opcodeใหม่.

**Failure mode:** อย่าเอา fetch→decode→executeเป็น timing modelจริงของ modern CPU.

**Reflection:** ISA vs microarchitectureต่างกันอย่างไร?

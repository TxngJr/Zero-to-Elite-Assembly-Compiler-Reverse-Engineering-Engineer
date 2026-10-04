# Worked Examples — Linker & Loader

## Example 1 — Static archive resolution

**Goal:** เห็นว่า archive membersถูกดึงเมื่อ symbolจำเป็น ไม่ใช่ copyทุก objectเสมอ.

**Command / action:**

```bash
make -C 07-linker-loader/projects/static-demo clean all
nm -A 07-linker-loader/projects/static-demo/*.a
file 07-linker-loader/projects/static-demo/*
```

จากนั้นรัน appที่ Makefileสร้างและ inspect:

```bash
nm -C 07-linker-loader/projects/static-demo/app 2>/dev/null || true
```

**Prediction:** archiveมีหลาย members; linkerเลือก definitionsเพื่อ resolve undefined references.

**Expected key evidence:** final executable behaviorผ่าน project test; symbolsจาก required memberปรากฏตาม build.

**What may vary:** symbol visibility/layout/LTO behaviorถ้า flagsเปลี่ยน.

**Explain:** static libraryคือ archive index + objects ไม่ใช่ runtime-loaded `.so`.

**Modification:** เพิ่ม unused function/objectใน archiveแล้วตรวจว่ามันเข้ final imageหรือไม่.

**Failure mode:** link orderของ static archivesมีผล; อย่าคิดว่า `-lA -lB` สลับได้เสมอ.

**Reflection:** อธิบาย one-pass-ish symbol resolution modelแบบ simplified.

---

## Example 2 — Shared object, DT_NEEDED, loader

**Goal:** เชื่อม `.so`, dynamic section, PLT/GOTและ runtime loader.

**Command / action:**

```bash
make -C 07-linker-loader/projects/shared-demo clean all

file 07-linker-loader/projects/shared-demo/*
readelf -dW 07-linker-loader/projects/shared-demo/app
readelf -rW 07-linker-loader/projects/shared-demo/app
objdump -d -Mintel 07-linker-loader/projects/shared-demo/app \
  | grep -A6 -B2 '@plt' || true
```

**Prediction:** appมี dynamic dependencyต่อ shared libraryและ relocations/import machinery.

**Expected key evidence:** `DT_NEEDED`/dynamic entries; call pathอาจผ่าน PLT.

**What may vary:** PLT style, RELRO/lazy-vs-now flagsตาม toolchain.

**Explain:** linkerสร้าง metadataให้ loaderแก้ runtime addresses; GOTเก็บ indirection slots, PLTช่วย call imported functionsใน common model.

**Modification:** รันด้วย `LD_DEBUG=libs,bindings` เฉพาะ course appเพื่อสังเกต loader messages.

**Failure mode:** อย่าตั้ง `LD_LIBRARY_PATH` ถาวรทั้งระบบเพื่อ lab; scopeให้ command/project.

**Reflection:** static linkกับ dynamic linkย้ายงานไป build/runtimeต่างกันอย่างไร?

---

## Example 3 — Relocation calculation model

**Goal:** คำนวณ relocationแบบ symbolicก่อนให้ codeยืนยัน.

**Command / action:**

```bash
make -C 07-linker-loader/projects/reloc-model clean test
07-linker-loader/projects/reloc-model/reloc-model
```

**Prediction:** relocation expressionเช่น PC-relativeขึ้นกับ S (symbol), A (addend), P (place).

**Expected key evidence:** simulator/testให้ค่าตรงสูตรที่บทกำหนด.

**What may vary:** noneใน deterministic model.

**Explain:** relocation typeกำหนด width/sign/formula ไม่ใช่ “ใส่ addressลงทุกที่”.

**Modification:** เปลี่ยน S/P/Aด้วยมือแล้วทำนาย overflow/range.

**Failure mode:** x86-64 PC-relative fieldบางชนิดมี signed 32-bit rangeจำกัด.

**Reflection:** ทำไม linkerอาจต้องใช้ different code model/thunksในระบบใหญ่?

---

## Example 4 — Constructor before main

**Goal:** เห็น runtime startupไม่ใช่ loaderกระโดดตรง `main`เสมอ.

**Command / action:**

```bash
gcc -O0 -g 07-linker-loader/examples/constructor.c -o /tmp/constructor
/tmp/constructor

readelf -SW /tmp/constructor | grep -E 'init|array'
readelf -dW /tmp/constructor | grep -E 'INIT|ARRAY' || true
```

**Prediction:** constructor outputเกิดก่อน main output.

**Expected key evidence:** init-array/runtime metadataรองรับ startup callbacks.

**What may vary:** exact startup symbols/sections.

**Explain:** ELF loader maps image แต่ language/runtime startup codeจัด constructorsก่อนเรียก user main.

**Modification:** เพิ่ม constructorสองตัวแล้วอย่า assume orderหากไม่ได้กำหนด priority/contract.

**Failure mode:** reverse engineer startup codeแล้วเข้าใจผิดว่าเป็น application main logic.

**Reflection:** เชื่อม Chapter 07กับ Chapter 16 RE “runtime noise”.

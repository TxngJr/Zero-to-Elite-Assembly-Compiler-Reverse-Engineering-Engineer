# Worked Examples — ELF Internals

## Example 1 — Relocatable object vs executable

**Goal:** แยก ELF Type, sections และ entry pointของ `.o` กับ final executable.

**Command / action:**

```bash
mkdir -p 06-elf/build
gcc -c -O0 -g 06-elf/examples/hello.c -o 06-elf/build/hello.o
gcc -O0 -g 06-elf/examples/hello.c -o 06-elf/build/hello

file 06-elf/build/hello.o 06-elf/build/hello
readelf -hW 06-elf/build/hello.o
readelf -hW 06-elf/build/hello
readelf -SW 06-elf/build/hello.o
readelf -lW 06-elf/build/hello
```

**Prediction:** objectเป็น `REL`; final executableอาจเป็น `DYN` (PIE) หรือ `EXEC`; objectไม่มี runtime program-header mappingแบบ final image.

**Expected key evidence:** `Type`, `Entry point`, section table และ program headersต่างกันตาม role.

**What may vary:** PIE defaultตาม distro/compiler.

**Explain:** sectionsใช้โดย linker/tools; segments/program headersบอก loaderว่าจะ map fileอย่างไร.

**Modification:** linkด้วย `-no-pie` แล้ว compare ELF Type/program headers.

**Failure mode:** อย่าสรุปว่า sectionหนึ่งเท่ากับ memory mappingหนึ่งเสมอ.

**Reflection:** `.text/.rodata/.data/.bss` มี file bytesและ memory permissionsต่างกันอย่างไร?

---

## Example 2 — Symbols + relocations ก่อน link

**Goal:** เห็น unresolved referenceใน objectจริง.

**Command / action:**

```bash
gcc -c -O0 -g 06-elf/examples/reloc_user.c \
  -o 06-elf/build/reloc_user.o
gcc -c -O0 -g 06-elf/examples/reloc_def.c \
  -o 06-elf/build/reloc_def.o

nm 06-elf/build/reloc_user.o
readelf -rW 06-elf/build/reloc_user.o
objdump -dr -Mintel 06-elf/build/reloc_user.o
```

**Prediction:** symbolที่ definedอีก objectหนึ่งยัง unresolvedใน user objectและมี relocation recordผูกกับ reference site.

**Expected key evidence:** `nm` แสดง undefined symbol; `readelf -r`/objdumpแสดง relocation type+symbol.

**What may vary:** relocation typeตาม code model/PIE flags.

**Explain:** assemblerยังไม่รู้ final address; linkerใช้ relocationเพื่อ patch field/compute displacement.

**Modification:** linkสอง objectsเข้าด้วยกันแล้วดู relocation/symbol statusใน final image.

**Failure mode:** undefined symbolใน `.o` ไม่ใช่ errorเสมอ; มันปกติถ้าจะ resolveตอน link.

**Reflection:** symbol tableกับ relocation tableตอบคำถามคนละอย่างอย่างไร?

---

## Example 3 — `.bss` file size vs memory size

**Goal:** เห็นว่า zero-initialized storageไม่ต้องเก็บ zero bytesทั้งหมดใน file.

**Command / action:**

```bash
gcc -O0 -g 06-elf/examples/sections.c -o 06-elf/build/sections
readelf -SW 06-elf/build/sections
readelf -lW 06-elf/build/sections
size 06-elf/build/sections
```

**Prediction:** `.bss` เป็น NOBITS/occupy memoryแต่ไม่เพิ่ม file payloadเท่าขนาด runtime storage.

**Expected key evidence:** section type/sizeและ LOAD segment FileSiz/MemSizอาจต่าง.

**What may vary:** section placement/alignment.

**Explain:** loader/kernelสร้าง zeroed memoryส่วนที่ MemSizเกิน FileSizตาม ELF mapping contract.

**Modification:** เพิ่ม static zero arrayใหญ่ใน local copyแล้ว compare file size vs `.bss` size.

**Failure mode:** อย่าอ่าน `.bss` bytesจาก file offsetเหมือน PROGBITS.

**Reflection:** ทำไมแนวคิดนี้สำคัญกับ kernel imageและlarge static buffers?

---

## Example 4 — Course ELF inspector vs readelf

**Goal:** cross-check parserที่เราเขียนเองกับ mature tool.

**Command / action:**

```bash
make -C 06-elf/projects/elf-inspector clean test
06-elf/projects/elf-inspector/elf-inspector \
  06-elf/projects/elf-inspector/test-fixture \
  > /tmp/our-elf.txt

readelf -hSW \
  06-elf/projects/elf-inspector/test-fixture \
  > /tmp/readelf.txt
```

ถ้ artifact namingต่าง ให้ดู project Makefile.

**Prediction:** class/endian/machine/section countหลักควรตรง.

**Expected key evidence:** parser reject malformed/truncated inputตาม testsและไม่อ่านเกิน buffer.

**What may vary:** formattingและรายละเอียดที่ toolเราไม่ implement.

**Explain:** binary parserต้อง validate offsets/countsก่อน pointer arithmetic/read.

**Modification:** copy fixtureแล้ว truncate file; parserควร fail cleanly.

**Failure mode:** parser output “บางอย่าง”ไม่เท่ากับ parseถูก; cross-check invariants.

**Reflection:** เขียน bounds checksที่ ELF section-table parserต้องมี.

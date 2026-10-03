# Theory — Linker & Loader

## 1. Linker Job

Linkerรับ `main.o + util.o + libraries` แล้ว collect sections, resolve symbols, decide layout/addresses, apply relocations และ emit executable/shared object.

Linkerจริงยังมี section GC, relaxation, LTO, scripts, TLS ฯลฯ.

## 2. Definitions and References

Object A define `foo`; Object B reference `foo`.

```bash
nm -g A.o B.o
```

`U` = undefined reference. Linkสำเร็จเมื่อ referencesที่ต้อง resolveหา definitionsได้ตาม rules.

## 3. Strong / Weak

Global strong definitionปกติชนะ weak definitionหนึ่งตัว. Multiple strong definitionsโดยทั่วไปเป็น link error. Weak symbolsเหมาะกับ default/optional hooksบางกรณีแต่มี platform semantics.

## 4. Static Archives

```bash
ar rcs libutil.a util.o helper.o
```

Archiveเป็น collectionของ object files. Linkerมัก extract memberเมื่อมี unresolved symbolที่ memberตอบได้. Traditional archive resolutionทำให้ library orderอาจสำคัญ.

## 5. Relocation Formulas

Notation:
- `S` symbol value
- `A` addend
- `P` relocation place

Toy formulas:

```text
ABS64 = S + A
PC32  = S + A - P
```

Real x86-64 typesมี width/range/PLT/GOT/TLS semanticsเพิ่ม.

## 6. Why PC-relative

`call rel32` และ RIP-relative dataใช้ displacementจาก place/current context. เมื่อ caller/targetย้ายด้วยกัน displacementอาจคงเดิม จึงช่วย position-independent code.

## 7. Static vs Dynamic Linking

Static linkingนำ library codeที่ต้องใช้เข้า outputโดยมาก. Dynamic linkingเก็บ dependency/symbol/relocation metadataให้ runtime loader map shared objectsและ resolve references.

Static executableยังพึ่ง kernel/syscall ABI.

## 8. Shared Objects and PIC

Shared libraryต้อง mapได้หลาย base addresses:

```bash
gcc -fPIC -c lib.c
gcc -shared -Wl,-soname,libdemo.so.1 -o libdemo.so.1 lib.o
```

PICใช้ RIP-relative/indirectionเพื่อหลีกเลี่ยง fixed absolute text addressesจำนวนมาก.

## 9. PIE

PIEเป็น position-independent executableเพื่อ ASLR. มักเป็น `ET_DYN`แต่มี executable startup semantics.

## 10. GOT

Global Offset Tableเก็บ addresses/data referencesที่ต้อง resolve/relocate. PIC codeใช้ GOT indirectionในหลายรูปแบบ.

## 11. PLT

Procedure Linkage Tableเป็น stub mechanismสำหรับ dynamic function calls. Modern optionsเช่น `-fno-plt` อาจเปลี่ยน shape จึงอย่าจำ disassemblyรูปเดียว.

## 12. Lazy vs Eager Binding

บาง function relocations resolveครั้งแรกที่ call (lazy) หรือ startup (eager เช่น `LD_BIND_NOW=1`). RELRO/hardeningเปลี่ยน writable relocation windows.

## 13. Dynamic Section

`readelf -d` แสดง tagsเช่น:
- `DT_NEEDED`
- `DT_SONAME`
- `DT_RPATH/DT_RUNPATH`
- relocation tables
- init/fini arrays

`DT_NEEDED` ปกติเก็บ dependency nameไม่ใช่ absolute path.

## 14. SONAME

SONAMEเป็น compatibility identityที่ dependent objectบันทึกใน `DT_NEEDED` เมื่อ libraryกำหนด. Filename/symlink/package conventionsเป็นอีก layer.

## 15. Runtime Search Path

Dynamic loader search rulesมีรายละเอียดและ secure-execution restrictions. Inputsสำคัญได้แก่ RPATH/RUNPATH, `LD_LIBRARY_PATH`ใน permitted contexts, loader cache/config และ default dirs.

Labใช้ `$ORIGIN` RUNPATHเพื่อ self-contained demo.

## 16. $ORIGIN

`$ORIGIN` หมายถึง directoryของ objectที่มี token. ต้อง quoteให้ shellไม่ expand:

```bash
-Wl,-rpath,'$ORIGIN'
```

## 17. Dynamic Loader

Kernelอ่าน `PT_INTERP` แล้วเริ่ม interpreter/dynamic loaderสำหรับ dynamic executable. Loader map dependencies, relocate, resolve, run initializers แล้วส่ง controlเข้าสู่ runtime startup.

## 18. ldd Safety

`ldd` เหมาะกับ course binariesที่เรา buildเอง. สำหรับไฟล์ไม่รู้จัก ให้เริ่มจาก `readelf -d`/controlled toolingแทนการ execute-oriented inspectionโดยไม่เข้าใจ provenance.

## 19. LD_DEBUG

บน glibc: `LD_DEBUG=libs,bindings` ช่วยเห็น search/binding details. Output platform-specificและใช้กับ course binaries.

## 20. Symbol Visibility

`default/hidden/protected` visibilityมีผลต่อ dynamic export/interposition. `-fvisibility=hidden`ช่วยลด exported surfaceเมื่อ libraryออกแบบ APIชัด.

## 21. Symbol Interposition

Default-visible symbolอาจถูกเลือกจาก objectอื่นตาม lookup scope/order. Compiler/linkerต้อง conservativeบางกรณีเพราะ function/dataอาจถูก interpose.

## 22. Copy/Text Relocations

Historical mechanismsบางแบบ copy dataหรือ patch text. Hardened buildsพยายามหลีกเลี่ยง writable/executable relocation patterns; เรียนเพื่ออ่าน diagnostics.

## 23. Constructors / init arrays

C constructor/C++ global initializationมักสร้าง `.init_array` entries. Runtimeเรียกก่อน `main`ตาม ordering constraints.

## 24. Kernel vs Loader vs Runtime vs libc

- kernel map executable/interpreterและสร้าง process
- dynamic loader map shared objects/relocate/resolve
- C runtimeเตรียม language runtimeแล้วเรียก main
- libcเป็น library APIs ไม่ใช่ loaderเอง

## 25. Runtime Mappings

`/proc/PID/maps` หรือ GDB `info proc mappings` แสดง mappingsจริง. เปรียบกับ `readelf -l` เพื่อเชื่อม segmentsกับ memory.

## 26. Linker Scripts Preview

Linker scriptควบคุม section placement, symbols, memory regions. สำคัญใน kernels/embedded; บทนี้เน้น intro.

## 27. Failure Taxonomy

- `undefined reference` — link-time resolution
- `multiple definition` — conflicting definitions
- `cannot open shared object file` — runtime search
- `symbol lookup error` — runtime resolution/version mismatch
- relocation overflow/truncated — valueไม่ fit encoding/range

## 28. Mental Checklist

input objects? symbols? archives? layout? relocations? static/shared? PIC/PIE? NEEDED/SONAME/RUNPATH? runtime mappings? binding timing?

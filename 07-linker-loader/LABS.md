# Labs

1. **Undefined reference:** compile `main_ref.c`โดยไม่ provider; ใช้ `nm`พิสูจน์ U.
2. **Resolution:** link providerเข้ามา; ดู transition U→defined.
3. **Multiple definition:** สร้าง strong definitionซ้ำใน lab copy; อ่าน diagnostic.
4. **Weak vs strong:** weak demo + strong override.
5. **Archive extraction:** `ar t`, `nm`, linker map.
6. **Relocations:** `objdump -dr` ก่อน linkเทียบ final disassembly.
7. **Toy formulas:** run reloc-model; คำนวณ S+A / S+A-P.
8. **Shared library:** inspect ET_DYN, SONAME, DT_NEEDED.
9. **RUNPATH:** หา `$ORIGIN`; ย้าย directoryทั้งชุดแล้ว run.
10. **GOT/PLT:** inspect app disassembly + relocations.
11. **PIE/non-PIE:** compare e_type/relocations.
12. **Lazy/eager:** `LD_DEBUG=bindings` กับ `LD_BIND_NOW=1` บน course binary.
13. **Constructors:** inspect `.init_array` และ runtime order.
14. **Runtime maps:** GDB `info proc mappings`; match app/libc/libcalc.
15. **Loader failure:** ซ่อน libraryชั่วคราว, observe error, diagnoseจาก dynamic metadata.

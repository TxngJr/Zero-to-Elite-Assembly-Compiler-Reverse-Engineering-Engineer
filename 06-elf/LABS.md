# Labs

1. **Magic & header:** build `hello.c`, ใช้ `xxd -l 64`, `readelf -h`, ระบุ magic/class/data/type/machine/entry.
2. **REL vs EXEC vs DYN:** inspect `.o`, `-no-pie` และ default PIE; ทำนาย `e_type`.
3. **Sections:** `sections.c`; หา `.text/.rodata/.data/.bss`.
4. **Segments:** `readelf -lW`; map sectionsเข้าสู่ `PT_LOAD`.
5. **Permissions:** หา LOAD segments R / R E / RW.
6. **BSS:** เพิ่ม zero arrayขนาดใหญ่; เปรียบ file sizeกับ `p_memsz`.
7. **Custom section:** หา `.course_meta` และ dumpด้วย `objdump -s -j`.
8. **Symbols:** compare `nm` กับ `readelf -s`.
9. **Relocations:** compile `reloc_user.c` แยก; ดู `readelf -r`, `objdump -dr`.
10. **Strip:** strip copyของ executable; compare `.symtab`, size, runtime.
11. **DWARF:** compare build `-g` และ no-debug.
12. **PIE:** compare defaultกับ `-no-pie`; discuss ASLR.
13. **PT_INTERP:** หา interpreter string.
14. **ELF Inspector:** อ่าน executable/object/shared objectและ cross-checkกับ readelf.
15. **Corrupt input:** feed text/truncated file; inspectorต้อง fail cleanly.

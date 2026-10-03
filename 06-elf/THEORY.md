# Theory — ELF Internals

## 1. ELF คือ container format

ELF เก็บ machine code, data, metadata, symbols, relocations, program headers และ section headers.

```text
source → compiler/assembler → ET_REL (.o) → linker → ET_EXEC/ET_DYN → loader → process image
```

## 2. Identification

4 bytesแรกคือ `7f 45 4c 46`. `e_ident` ยังบอก ELF32/64, byte order, version และ OS ABI field. Course targetคือ ELF64 little-endian x86-64.

## 3. File types

- `ET_REL` relocatable object
- `ET_EXEC` executable
- `ET_DYN` shared object **และ PIE executableจำนวนมาก**
- `ET_CORE` core dump

ดังนั้น `ET_DYN` ไม่ได้แปลว่า libraryเสมอ.

## 4. ELF64 Header

Fieldsสำคัญ:
- `e_type`, `e_machine`
- `e_entry`
- `e_phoff/e_phnum/e_phentsize`
- `e_shoff/e_shnum/e_shentsize`
- `e_shstrndx`

`e_entry` เป็น virtual address—not file offset.

## 5. Program Headers: loader view

`PT_LOAD` บอก mapping:

```text
file p_offset → virtual p_vaddr
p_filesz bytes from file
p_memsz bytes in memory
p_flags permissions
p_align alignment
```

ถ้า `p_memsz > p_filesz` ส่วนเพิ่มเป็น zero-filled storage conceptually.

Typesที่พบบ่อย: `PT_INTERP`, `PT_DYNAMIC`, `PT_PHDR`, `PT_NOTE`, `PT_GNU_STACK`, `PT_GNU_RELRO`.

## 6. Section Headers: linker/tool view

Sectionsจัดข้อมูลเชิง logical:
- `.text` code
- `.rodata` constants
- `.data` initialized writable data
- `.bss` zero storage / `SHT_NOBITS`
- `.symtab/.strtab`
- `.dynsym/.dynstr`
- `.rela.*`
- `.eh_frame/.debug_*`

Runtime loaderไม่ได้ map section-by-section; มัน map **segments**.

## 7. Sections vs Segments

หนึ่ง `PT_LOAD` segmentครอบหลาย sectionsได้. Sectionsเป็น logical/link-time view; segmentsเป็น runtime mapping units.

## 8. Section Names

`e_shstrndx` ชี้ section-string-table section. `sh_name` เป็น offsetเข้า string table ไม่ใช่ pointer.

## 9. BSS / NOBITS

`.bss` สามารถมี `sh_size` ใหญ่โดยไม่เพิ่ม file bytesเท่ากัน. จึง:

```text
file size != runtime memory footprint
```

## 10. Symbols

`Elf64_Sym` มี `st_name, st_info, st_shndx, st_value, st_size`.

Bindings: LOCAL, GLOBAL, WEAK. Types: FUNC, OBJECT, SECTION, NOTYPE.

## 11. symtab vs dynsym

`.symtab` มักละเอียดกว่าและ stripออกได้. `.dynsym` เก็บ subsetที่ dynamic loaderต้องใช้. Stripped executableยังรันได้.

## 12. Undefined Symbols

Relocatable objectมี `UND` ได้ตามปกติเมื่อ definitionอยู่อีก object/library. มันยังไม่ใช่ link errorจนถึงขั้นที่ต้อง resolveแล้วหาไม่ได้.

## 13. Relocations

Assemblerไม่รู้ final addressทุก symbol จึงสร้าง relocation recordให้ linker patchภายหลัง.

Notation:
- `S` symbol value
- `A` addend
- `P` relocation place

Formulaจริงขึ้นกับ relocation type; Chapter 07ลงลึก.

## 14. File Offset vs Virtual Address

อย่าสลับ:
- file offset = byte locationใน file
- virtual address = addressใน process mapping
- section offset = file locationของ section
- relocation offset = patch placeตาม context

## 15. Entry Point

`e_entry` คือ addressเริ่ม control-flowของ image model. โดยทั่วไปไม่ใช่ `main`; C runtime startupอยู่ก่อน main.

## 16. PIE vs non-PIE

Modern Linux toolchainsมัก default PIE: PIE executableมัก `ET_DYN`; `-no-pie` มัก `ET_EXEC`. PIEช่วย ASLR.

## 17. Dynamic Metadata Preview

`readelf -d` แสดง `DT_NEEDED`, string tables, relocations, init/fini arrays และ tagsอื่น. Chapter 07เชื่อม metadataกับ dynamic loader.

## 18. Notes / GNU Extensions

`.note.*` อาจเก็บ build ID/ABI notes. `GNU_STACK` และ `GNU_RELRO` สื่อ runtime/hardening properties.

## 19. Debug Sections

`-g` เพิ่ม DWARF `.debug_*` sections. Loaderไม่ต้อง map debug infoเพื่อ execute programปกติ.

## 20. Safe Binary Parsing

Parserต้อง validate:
1. minimum file size
2. magic/class/endian/version
3. entry sizes
4. integer overflow
5. `offset + count*entry_size` อยู่ใน file
6. indicesอยู่ใน bounds
7. string offsetsมี NULภายใน table

อย่า cast arbitrary bytesแล้วเดิน offsetsต่อโดยไม่ตรวจ.

## 21. Tool Workflow

```bash
file a.out
readelf -h a.out
readelf -l a.out
readelf -S a.out
readelf -s a.out
readelf -r object.o
readelf -d a.out
objdump -d -Mintel a.out
nm -n a.out
size a.out
strings -a a.out
```

## 22. Mental Checklist

type/class/machine? entry? PHDRs? LOAD permissions? sections? symbols? relocations? dependencies? debug info? PIE/stripped?

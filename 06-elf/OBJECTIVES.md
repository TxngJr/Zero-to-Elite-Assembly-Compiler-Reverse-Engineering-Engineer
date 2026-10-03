# Objectives

เมื่อจบบทนี้ควรสามารถ:

- อธิบาย ELF file types: relocatable, executable, shared object, core
- อ่าน ELF identification bytes และ ELF64 header
- แยก **sections** ออกจาก **segments**
- อธิบายว่า loader สนใจ program headers ขณะที่ linker/debugger มักใช้ sections/symbols มาก
- อ่าน `PT_LOAD`, permissions, file size vs memory size
- อธิบาย `.text`, `.rodata`, `.data`, `.bss`, `.symtab`, `.strtab`, `.dynsym`, `.dynstr`
- แยก static symbol table กับ dynamic symbol table
- อ่าน relocation entries ระดับ concept
- อธิบาย `NOBITS` และเหตุผลที่ `.bss` ใช้ memory มากกว่า bytes ใน file ได้
- ใช้ `file`, `readelf`, `objdump`, `nm`, `size`, `strings`
- เชื่อม virtual address, file offset และ load segment
- เขียน ELF64 inspector ขนาดเล็กที่ตรวจ bounds ก่อนอ่าน structures

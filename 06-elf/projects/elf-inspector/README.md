# ELF Inspector Project

Educational ELF64 readerสำหรับ Chapter 06.

รองรับ ELF64 little-endian conventional header counts, program-header summary และ section names/sizes พร้อม defensive range checks.

ตั้งใจไม่รองรับ ELF32, big-endian, extended numbering (`PN_XNUM`, extended `e_shnum`, `SHN_XINDEX`) หรือทุก vendor extensionในเวอร์ชันนี้. Formatนอก scopeต้องถูก rejectแทนอ่านต่อด้วย assumptionsผิด.

```bash
make test
./elf-inspector /bin/ls
```

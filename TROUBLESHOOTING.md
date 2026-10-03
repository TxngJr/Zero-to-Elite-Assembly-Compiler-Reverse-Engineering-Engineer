# Troubleshooting

## gcc / clang / readelf / objdump not found
Fedora: run `./scripts/install-fedora-tools.sh`. GNU ELF toolsมาจาก `binutils`.

## Permission deniedตอน run script
ตรวจ execute bitด้วย `ls -l`, filesystem `noexec`ด้วย `findmnt -T . -o OPTIONS`.

## GDB says no debugging symbols
Buildด้วย `-g`; optimized codeยังอาจมี `<optimized out>`.

## Assembly operand size mismatch
ตรวจ register/memory widthsและ BYTE/WORD/DWORD/QWORD PTR.

## Function C↔Assembly crash
ตรวจ SysV AMD64 callee-saved registers, stack restore/alignment, prototype widths.

## Raw syscall arg4ผิด
Linux x86-64 arg4อยู่ R10; `syscall` clobber RCX/R11.

## ELF inspector rejects a valid exotic ELF
Course inspector intentionallyรองรับ ELF64 little-endian conventional countsเท่านั้น. ใช้ `readelf`/elfutilsสำหรับ ELF32, big-endian หรือ extended numbering.

## readelf sectionกับ runtime mappingดูไม่ตรง
Loader map **segments** ไม่ใช่ section-by-section. ใช้ `readelf -lW` และ section-to-segment mapping.

## undefined reference
นี่เป็น link-time symbol resolution failure: ใช้ `nm`, `readelf -s`, ตรวจ object/library orderและ definitions.

## cannot open shared object file
ตรวจ `readelf -d app`, `DT_NEEDED`, SONAME, RUNPATH/RPATH และ loader search. อย่า copy .soสุ่มเข้า system directories.

## $ORIGINหายจาก linker option
Quoteเป็น `'$ORIGIN'` (หรือ escapeตาม shell/build system) เพื่อไม่ให้ shell expandก่อนถึง linker.

## GDB batch testถูก skip
Chapter 08 testจะ skip debugger-specific assertionถ้า environmentไม่มี `gdb`; Fedora course machineควรติดตั้ง GDBผ่าน installerแล้ว run `make inspect`/GDB labsเอง.

## GDB ptrace permission error
Container/security policyอาจห้าม ptrace. อย่าปิด security controlsแบบสุ่ม; ใช้ local Fedora environmentที่อนุญาต debuggingของ processตัวเอง.

## ไม่มี core fileหลัง crash
ตรวจ `ulimit -c` และ Fedora/systemd-coredump config. ใช้ `coredumpctl list/info/debug` เมื่อระบบใช้ systemd-coredump. GDB direct crash labใช้แทนได้.

## perf permission denied
perfเป็น optional. ตรวจ policy/kernel settings; ไม่ต้องลด securityเพียงเพื่อให้ testsผ่าน.

## Sanitizer reportยาว
อ่าน error class → first relevant source frame → invalid operation/address → allocation/free origin → root cause → fix → rerun.

## make missing separator
Recipe lineต้องเริ่ม TABจริง.

## GCC/Clang outputต่างกัน
Compilerมี diagnostics/codegenต่างกันได้. ยึด language/ABI/ELF contracts + tests + runtime evidence.

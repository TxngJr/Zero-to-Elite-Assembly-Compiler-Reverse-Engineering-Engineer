# Troubleshooting

## `gcc: command not found`
ตรวจ `command -v gcc`; Fedoraติดตั้งด้วย `./scripts/install-fedora-tools.sh` หรือ `sudo dnf install gcc`.

## `Permission denied` ตอนรัน script
ตรวจ execute bitด้วย `ls -l`; ใช้ `chmod +x script.sh` หรือ `bash script.sh`. ถ้า filesystemเป็น `noexec` ให้ตรวจ `findmnt -T . -o OPTIONS`.

## GDB ไม่มี symbols / variable optimized out
ใช้ `-g`; สำหรับ labแรกลอง `-O0` แต่จำว่า optimizerไม่รับประกัน source variableต้องมี storage slot.

## `readelf` / `objdump` / `as` ไม่พบ
Fedora packageหลักคือ `binutils`.

## Assembly error: operand size mismatch
ตรวจ widthของ register/memory operandและใส่ `BYTE/WORD/DWORD/QWORD PTR` เมื่อ assembler inferไม่ได้.

## Assembly รันแล้วค่าด้านบนของ RAXหาย
การเขียน EAX zero-extendsไป RAX. ถ้าตั้งใจแก้เฉพาะ 8/16 bitsให้ตรวจ AL/AX semantics.

## Function C↔Assembly crashแบบสุ่ม
ตรวจ System V AMD64 ABI: callee-saved registers, stack restore, alignmentก่อน nested call และ prototype/type width.

## Raw syscallใช้ arg4แล้วผลแปลก
Linux x86-64 syscall arg4ใช้ R10 ไม่ใช่ RCX; `syscall` clobber RCX/R11.

## `_start` binary segfaultเมื่อใส่ message length symbol
ใน GNU Intel syntax symbol expressionอาจถูกตีความเป็น memory operand. ตรวจ disassembly; ใช้ immediate syntaxเช่น `OFFSET`เมื่อจำเป็นและยืนยัน bytesด้วย `objdump -d -Mintel`.

## `perf stat` ขึ้น permission denied / not supported
perfเป็น optional lab. ตรวจ `kernel.perf_event_paranoid`, container/VM restrictions และ policyของเครื่อง; ไม่ต้องลด security settingเพียงเพื่อให้บทผ่าน.

## `make: *** missing separator`
Make recipeต้องขึ้นต้นด้วย TABจริง.

## Sanitizer report ยาว
อ่าน error class → source frameแรกของเรา → address/operation → allocation/free history → root cause → fix → rerun.

## GCC/Clang diagnosticsต่างกัน
Compilerสามารถเตือนต่างกันได้. ใช้ language/ABI contract, tests และ inspectionเป็นหลัก ไม่คาด wordingเหมือนกัน.

# Labs

1. **Register width:** `rax=-1` แล้วเขียน EAX/AX/AL; inspect upper bitsด้วย GDB.
2. **Assemble/link/disassemble:** สร้าง `.o` จาก `exit_code.s`, ดู `objdump -dr`, link final executable.
3. **Arithmetic/flags:** step `arithmetic.s`, ทำนาย EAX และ inspect EFLAGS.
4. **Signed vs unsigned:** เปรียบเทียบ pattern `0xFFFFFFFF` กับ 1 โดย `jl` และ `jb`.
5. **TEST:** ใช้ `test eax,eax` กับ zero/negative patterns.
6. **Addressing:** คำนวณ `[rdx+rcx*4]` ด้วยมือแล้วตรวจ GDB.
7. **LEA vs load:** เปรียบเทียบ `lea rax,[rdi+8]` กับ `mov rax,[rdi+8]`.
8. **SHR vs SAR:** ทำนาย negative pattern ก่อนรัน.
9. **Loop:** sum 1..10 ทั้ง count-up และ count-down.
10. **CMOV:** max แบบ branch และ `cmovg`; เปรียบเทียบ correctness ไม่สรุป performanceจาก syntax.
11. **Stack trace:** push/pop แล้วดู RSP/memory; restoreก่อน return.
12. **CALL/RET:** วาด return address/RSP แล้วตรวจ GDB.
13. **Sections:** วาง dataใน `.rodata/.data/.bss` แล้วใช้ `readelf -S/-s`.
14. **Array Kernels:** ทำ project แล้ว unroll sum loop 2 elementsโดย handle odd count.
15. **Compiler comparison:** C array sum ที่ `-O0`/`-O2 -S -masm=intel`; annotate load/add/cmp/branch shapes.

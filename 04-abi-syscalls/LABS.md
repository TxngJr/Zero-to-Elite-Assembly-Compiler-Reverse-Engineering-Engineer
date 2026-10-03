# Labs

1. **Six arguments:** `abi_args.s` ตรวจ RDI,RSI,RDX,RCX,R8,R9.
2. **Stack arguments:** `sum_eight` inspect `[rsp+8]`, `[rsp+16]` ที่ entry.
3. **Callee-saved:** ทำสำเนา labที่ intentionallyไม่ restore RBX, สังเกต violation แล้วแก้กลับ.
4. **Stack alignment:** จด `rsp & 15` ก่อน nested callและที่ callee entry.
5. **Frame pointer:** C `-O0 -fno-omit-frame-pointer` เทียบ `-O2`.
6. **Red zone:** leaf function เทียบกับ `-mno-red-zone`.
7. **ABI Lab:** annotate `dot_i64` และ `call_twice` ว่า registerใด caller/callee-saved.
8. **Raw hello:** build `syscall_hello.s` ด้วย `-nostdlib -static` และ inspect `_start`.
9. **strace:** `strace -e write,exit ./build/syscall-hello` ถ้ามี tool.
10. **Raw error:** syscall-cat กับ nonexistent path; inspect negative RAXก่อน mappingเป็น exit status.
11. **Partial write:** cap write chunkในสำเนา lab; outputต้องยัง byte-perfect.
12. **argc/argv:** breakpoint `_start`, inspect initial stack/string pointers.
13. **RCX/R11:** ทำ harmless syscallแล้ว inspect register changes.
14. **syscall-cat:** test empty, text และไฟล์ใหญ่กว่า buffer.
15. **libc vs raw:** C `write()` เทียบ strace/disassemblyกับ raw syscall example.

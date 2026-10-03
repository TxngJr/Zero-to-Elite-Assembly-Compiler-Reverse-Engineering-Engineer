# Objectives

เมื่อจบบทนี้ควรสามารถ:
- อธิบายว่า ABI ต่างจาก ISA และ C languageอย่างไร
- ใช้ integer/pointer argument registers RDI,RSI,RDX,RCX,R8,R9 และ stack arguments
- อธิบาย return value ผ่าน RAX และ aggregate/FP caveatsระดับเริ่มต้น
- แยก caller-saved / callee-saved registers
- รักษา stack alignmentก่อน `call`
- สร้าง/อ่าน stack frame และเข้าใจ frame-pointer omission
- อธิบาย red zone พร้อมข้อจำกัด
- interoperate ระหว่าง C และ assembly
- อธิบาย Linux x86-64 syscall register convention ซึ่งต่างจาก function ABI
- ใช้ `syscall`, ตรวจ negative error return และใช้ `strace` เป็น evidence
- อ่าน process-entry stack (`argc/argv`) ในโปรแกรม `_start` แบบ no-libc
- เขียน file I/O loopที่รับมือ partial write

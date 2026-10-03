# Objectives

เมื่อจบบทนี้ควรสามารถ:

- อ่าน register families ของ x86-64 และอธิบายผลของการเขียน 32-bit subregister
- แยก immediate, register และ memory operand
- ใช้ `mov`, arithmetic, bitwise, shifts, compare/test
- reason จาก RFLAGS ไปสู่ signed/unsigned conditional jumps
- ใช้ addressing form `base + index*scale + displacement`
- ใช้ RIP-relative addressing สำหรับ static data
- เขียน labels, loops, branches และ conditional move
- อธิบาย `lea` ว่าคำนวณ effective address ไม่ได้ dereference memory
- อธิบาย `push/pop/call/ret` ระดับ instruction โดยยังไม่ปนกับ ABI rules
- inspect machine code ด้วย `objdump -d -Mintel` และ step ด้วย GDB
- เชื่อม C types/arrays จาก Chapter 02 เข้ากับ byte/word/dword/qword memory operations

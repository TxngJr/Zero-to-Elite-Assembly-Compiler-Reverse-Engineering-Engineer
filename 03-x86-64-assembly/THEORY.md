# Theory — x86-64 Assembly

## 1. ISA, assembly และ machine code
x86-64 คือ instruction-set architecture (ISA). Assembly เป็น human-readable notation; assembler แปลงเป็น object bytes แล้ว linker สร้าง executable. x86 instructions มีความยาวแปรผัน.

## 2. Intel syntax
คอร์สใช้ `.intel_syntax noprefix` และ destination-first เช่น `mov eax,42`. GNU `objdump -Mintel` ทำให้ disassembly สอดคล้องกัน. AT&T syntax ยังพบมากใน ecosystem แต่ semantics ISA เหมือนกัน.

## 3. Register families

```text
64: RAX RBX RCX RDX RSI RDI RBP RSP R8..R15
32: EAX EBX ECX EDX ESI EDI EBP ESP R8D..R15D
16: AX  BX  CX  DX  SI  DI  BP  SP  R8W..R15W
 8: AL  BL  CL  DL  SIL DIL BPL SPL R8B..R15B
```

การเขียน 32-bit register zero-extend ไปยัง parent 64-bit; การเขียน 8/16-bit ไม่ทำเช่นนั้น. `AH/BH/CH/DH` มี encoding caveats กับ REX prefixes.

## 4. Operands และ sizes
- immediate: `mov eax,42`
- register: `mov eax,ecx`
- memory: `mov eax,DWORD PTR [rdx]`

`[rbx]` คือ dereference memory ไม่ใช่ “ค่าใน RBX”. Size keywords ได้แก่ BYTE/WORD/DWORD/QWORD PTR.

## 5. MOV และ extension
`movzx` zero-extend; `movsx/movsxd` sign-extend. Pattern `0xFF` จึงเป็น 255 เมื่อ zero-extend และ -1 เมื่อ sign-extendจาก int8 representation.

## 6. Arithmetic
`add/sub/inc/dec/neg/imul`. `div/idiv` ใช้ implicit dividend registers และต้องเตรียม high half ให้ถูก; signed division มักใช้ `cdq/cqo` ก่อน `idiv` ตาม width.

## 7. RFLAGS
Flags ที่เน้น: ZF zero, SF sign, CF carry/borrowสำหรับ unsigned reasoning, OF signed overflow. `cmp a,b` set flagsเหมือนคำนวณ `a-b` โดยไม่เก็บผล. `test a,b` set flagsจาก AND โดยไม่เก็บผล.

## 8. Conditional jumps
Equality: `je/jne`. Unsigned: `ja/jae/jb/jbe`. Signed: `jg/jge/jl/jle`. `cmp` ไม่ได้มี signedness ฝังอยู่; condition codeที่ตามมาตีความ flags.

## 9. Labels/control flow
Labels กลายเป็น offsets/symbols. Branchesสร้าง CFG. วิเคราะห์ `cmp/test + jcc` เป็นคู่.

## 10. Zeroing idiom
`xor eax,eax` ทำ RAX เป็นศูนย์เพราะ 32-bit write zero-extends แต่ flags ต่างจาก `mov eax,0`.

## 11. Addressing
รูปแบบสำคัญ `[base + index*scale + displacement]`, scale ∈ {1,2,4,8}. `int32_t a[i]` มักใช้ `[base+index*4]`; `int64_t` ใช้ scale 8.

## 12. LEA
`lea rax,[rdi+rsi*4+8]` คำนวณ effective address expression โดยไม่อ่าน memory. จึงพบ LEA ใน arithmetic ด้วย.

## 13. RIP-relative addressing
`lea rdx, values[rip]` อ้าง static data แบบสัมพันธ์กับ instruction pointer ช่วย relocatable/PIC-friendly code.

## 14. Bitwise/shifts
`and/or/xor/not`, `shl/sal`, `shr`, `sar`, `rol/ror`. SHRเติม 0; SAR copy sign bit. Variable shift countใช้ CL ใน instruction formsทั่วไป.

## 15. CMOV/SETcc
`cmovcc` copyตาม flags โดยไม่ branch; `setcc` เขียน 0/1 ลง byte destination. Branchless ไม่ได้แปลว่าเร็วกว่าทุก workload.

## 16. Stack instructions
Simplified model: `push rax` ลด RSP 8 แล้ว store; `pop rax` load แล้วเพิ่ม RSP 8. Exact exception detailsเป็น ISA-level nuance.

## 17. CALL/RET
Simplified: CALL push return addressและ transfer control; RET pop return addressไป instruction pointer. Argument registers, preserved registers และ stack alignmentเป็น ABI—not CALL instruction itself.

## 18. Sections/directives
`.text`, `.rodata`, `.data`, `.bss`, `.global`, `.type`, `.size`, `.byte/.word/.long/.quad`, `.align`. Directivesเป็นคำสั่ง assembler ไม่ใช่ CPU instruction.

## 19. Inspect object

```bash
gcc -c example.s -o example.o
readelf -S example.o
readelf -s example.o
objdump -dr -Mintel example.o
nm example.o
```

## 20. GDB instruction workflow
`disassemble /r`, `info registers`, `x/16xb`, `si`, `ni`, `display/i $pc`. `si` stepเข้า call; `ni` next instruction.

## 21. SIMD preview
x86-64 ยังมี XMM/YMM/ZMM และ SSE/AVX families. บทนี้ตั้งใจเริ่ม scalar ก่อน; อย่าคิดว่า ISA มีเพียง GPRs.

## 22. Mental checklist
ถามทุก instruction: width? valueหรือdereference? signednessมีผลตรงไหน? flagsถูกอ่าน/เขียน? effective address? implicit registers? next control-flow edge?

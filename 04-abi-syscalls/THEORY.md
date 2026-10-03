# Theory — ABI & Linux Syscalls

## 1. ISA vs ABI vs API
- **ISA:** CPU instructions/registers/architectural state
- **ABI:** binary contractระหว่าง compiled components เช่น register passing, stack constraints และ object-format conventions
- **API:** source-level interface เช่น C function prototype

C function `long f(long,long)` ไม่บอกเองว่าใช้ RDI/RSI; ABIเป็นตัวกำหนดบนแพลตฟอร์มนี้.

## 2. System V AMD64 integer/pointer arguments

```text
1 RDI
2 RSI
3 RDX
4 RCX
5 R8
6 R9
7+ stack
return: RAX (กรณี scalar integer/pointerทั่วไป)
```

Floating-point/vector argumentsใช้ XMM registersตาม classification rules; aggregate typesมีรายละเอียดมากกว่าตารางนี้.

## 3. Stack arguments
ที่ function entry หลัง `call`, `[rsp]` คือ return address. สำหรับ integer args 7/8 แบบง่าย: `[rsp+8]` และ `[rsp+16]`. เมื่อ functionเปลี่ยน RSP offsetsต้องคำนวณใหม่.

## 4. Return values
Scalar integer/pointerทั่วไปใน RAX; 32-bit integerมัก EAX. Larger aggregatesอาจใช้หลาย registersหรือ hidden pointer จึงห้ามสรุปว่าทุก returnอยู่ RAX.

## 5. Caller-saved vs callee-saved
**callee-saved:** RBX, RBP, R12–R15 และต้อง restore RSP  
**caller-saved:** RAX, RCX, RDX, RSI, RDI, R8–R11

หาก calleeใช้ callee-saved registerต้อง save/restore. Callerที่ต้องใช้ค่า caller-savedหลัง callต้องเก็บเอง.

## 6. Stack alignment
ก่อน executing `call`, callerจัด RSPให้ 16-byte aligned. CALL push return address 8 bytes จึงทำให้ function entryโดยทั่วไปเห็น `rsp % 16 == 8`. ถ้า calleeจะ callต่อ ต้องปรับ alignmentก่อน callนั้น.

## 7. Prologue/epilogue
Classic frameคือ `push rbp; mov rbp,rsp; sub rsp,N ... leave; ret` แต่ compilerอาจ omit RBP, inline หรือไม่มี frameเลย. ABIไม่ได้บังคับ classic prologue.

## 8. Red zone
System V AMD64 user-space ABI มี 128-byte red zoneใต้ RSPที่ leaf functionใช้ได้ภายใต้ ABI assumptions. Kernel codeไม่ควรพึ่ง user-space red zone; kernel buildsมักใช้ `-mno-red-zone`.

## 9. Direction Flag
ABIคาด DF clearเมื่อเข้า/ออก function. ถ้าใช้ `std` ต้อง restoreด้วย `cld` ก่อนคืน callerที่คาด ABI-compatible state.

## 10. Variadic preview
Variadic callsเช่น `printf` มี rulesเพิ่ม; จำนวน vector registersสำหรับ variadic FP argsสื่อผ่าน AL. อย่าเดา variadic assembly calls.

## 11. C ↔ Assembly interop
C declarationบอก source signature; assembly export symbolและต้อง obey ABIเอง. Linkerไม่พิสูจน์ว่า implementation preserve registers/alignmentถูกต้อง.

## 12. Function pointers
`call rbx` เป็น indirect call. Target functionยังใช้ ABIเดิม; callerต้องจัด args, alignment และ saved stateเหมือน direct call.

## 13. Linux syscall boundary
Function ABI กับ syscall ABIไม่เหมือนกัน. Linux x86-64 raw syscall:

```text
RAX = syscall number
RDI = arg1
RSI = arg2
RDX = arg3
R10 = arg4
R8  = arg5
R9  = arg6
RAX = return / negative -errno on failure
```

Arg4ใช้ R10 เพราะ `syscall` clobber RCX/R11.

## 14. `syscall` clobbers
RCXรับ return RIPและ R11เกี่ยวกับ saved RFLAGSใน instruction mechanism; user codeต้องถือว่า RCX/R11ถูก clobber.

## 15. Raw errors vs libc
Raw syscallมักคืน negative `-errno`; libc wrapperปกติคืน `-1` และ set thread-local `errno`. อย่าเอา raw ABIไปเท่ากับ libc semanticsโดยตรง.

## 16. Syscall numbersที่ใช้ในคอร์ส
สำหรับ Linux x86-64: `read=0`, `write=1`, `close=3`, `exit=60`, `openat=257`. ตัวเลขนี้ OS+architecture-specific.

## 17. `_start` vs `main`
`main` ถูก C runtimeเรียก. `-nostdlib` binaryสามารถเริ่มที่ `_start`. Simplified initial stackก่อนแก้ RSP:

```text
[rsp]      argc
[rsp+8]    argv[0]
[rsp+16]   argv[1]
...
```

จริงยังมี envp และ auxiliary vectorต่อท้าย.

## 18. Partial I/O
`read` คืน 0 = EOF. `write` อาจคืนจำนวน bytesน้อยกว่าที่ขอโดยไม่ถือว่า error; robust loopต้อง advance pointerและลด remaining.

## 19. EINTR
System callsอาจถูก interruptและคืน EINTR. Production wrappersมัก retryตาม operation semantics. Challengeจะเพิ่ม EINTR handlingให้ training project.

## 20. `strace`
`strace` เป็น evidenceของ syscall boundary เช่น `openat/read/write/close/exit`; มัน decode callsให้มนุษย์อ่านง่าย ไม่ใช่ raw register traceทุกกรณี.

## 21. Unwinding
Hand assemblyในงานจริงอาจต้อง CFI/debug metadataเพื่อ backtraceที่ดี. `.type/.size` ช่วย symbol information; เราจะกลับมาลึกใน debugging chapter.

## 22. ABI checklist
signature/types → arg locations → return → callee-saved clobbers → nested calls → stack alignment → restoreทุก path → indirect/variadic/vector caveats.

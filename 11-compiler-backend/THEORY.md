# Theory — Compiler Backend

## 1. Backend Responsibilities

Backendเปลี่ยน target-independent/target-light IRเป็น target-specific code:
- instruction selection
- ABI lowering
- stack-frame layout
- register allocation/spilling
- branch/label emission
- machine/assembly emission

## 2. Instruction Selection

Elite IR:
```text
%t3 = bin + a b
```

Baseline x86-64:
```asm
mov rax, [slot_a]
mov rcx, [slot_b]
add rax, rcx
mov [slot_t3], rax
```

รุ่นนี้เลือก sequenceตรงไปตรงมาก่อน optimization.

## 3. Stack-Slot Baseline

ทุก source variable/tempมี 8-byte stack slot. ข้อดี:
- implementationเข้าใจง่าย
- callsไม่ทำลาย valuesเพราะ valuesอยู่ memory
- debuggingง่าย

ข้อเสีย: loads/storesเยอะและ frameใหญ่.

## 4. Frame Layout

Generated function:

```asm
push rbp
mov rbp, rsp
sub rsp, FRAME
...
leave
ret
```

FRAME roundขึ้นเป็น multiple of 16 เพื่อให้ stack alignmentก่อน callsถูกหลัง prologueนี้.

## 5. ABI Arguments

SysV integer arguments 1–6:
```text
RDI RSI RDX RCX R8 R9
```

callee copyเข้า local slots. Arguments 7+อ่านจาก `[rbp+16]`, `[rbp+24]`, ...

## 6. Caller Stack Arguments

Caller push stack argsจากขวาไปซ้าย. ถ้าจำนวน stack argsเป็น odd baseline backendใส่ 8-byte padding **ก่อน pushes** เพื่อให้ RSP aligned 16ก่อน `call` และ arg7ยังอยู่ `[callee rbp+16]`.

## 7. Return Values

EliteLang int/boolใช้ RAX. `main` returnค่าที่ OSเห็นเป็น process status low bitsตาม C runtime conventionsเมื่อ linkedผ่าน compiler driver.

## 8. Arithmetic

- add → `add`
- subtract → `sub`
- multiply → two-operand `imul`
- unary minus → `neg`

## 9. Signed Division / Modulo

```asm
mov rax, dividend
cqo
idiv rcx
```

quotientใน RAX; remainderใน RDX. Division by zeroยัง trapที่ runtime; optimizerห้าม foldผ่าน trapแบบไม่ระวัง.

## 10. Comparisons

```asm
cmp rax, rcx
setl al
movzx rax, al
```

EliteLang intsเป็น signed 64-bit modelใน backend จึงใช้ signed condition codesสำหรับ `< <= > >=`.

## 11. Boolean Representation

Baselineใช้ 0=false, 1=true. Type checkerรับประกัน boolean-producing operations. Control flowใช้ `test value,value`.

## 12. Branches

IR labels mapเป็น assembler local labels scopedด้วย function prefix:

```text
.L_main_while_cond1
```

ช่วยป้องกัน collisionข้าม functions.

## 13. Short Circuit

Chapter 10 lower `&&/||`เป็น CFGแล้ว backendเพียง emit jumps. นี่ทำให้ backendไม่ต้องรู้ source operator semanticsทุกอย่าง.

## 14. Calls

IR callเก็บ resultลง slotหลัง `call`. เนื่องจาก live valuesถูก spilledอยู่แล้ว caller-saved clobbersไม่ทำลาย compiler state.

## 15. Recursion

Recursionใช้ ABIเดียวกับ normal call; stack frameใหม่ถูกสร้างทุก invocation. `fact` testพิสูจน์ recursive calls.

## 16. More Than Six Arguments

`sum8` testบังคับ backendให้ handle both register argsและ stack args. นี่เป็น ABI regression testสำคัญ.

## 17. Virtual Registers

IR tempsเช่น `%t7` คือ unbounded virtual names. Real CPU registersมีจำกัด; allocatorต้อง map virtual→physicalหรือ spill.

## 18. Liveness for Allocation

Interferenceเกิดเมื่อสอง values liveพร้อมกันและจึงไม่ควรใช้ physical registerเดียวในช่วงนั้น.

## 19. Interference Graph

Node = virtual register/value. Edge = live overlap. Graph coloring assign colors=physical registers. Spillเมื่อ colorไม่พอ.

## 20. Linear Scan

Linear scanใช้ live intervalsเรียงตาม program positions. เร็วและเหมาะ JIT/simple compilers แต่ code qualityอาจด้อย graph coloring.

## 21. Spilling

Spillเก็บ valueใน stack. Backendปัจจุบันคือ “spill everything” baseline จึง correctแต่ช้า—จุดเริ่มที่ดีสำหรับ allocator challenge.

## 22. Register Classes

x86มี GPR/XMM/etc. Type/operationกำหนด register class. EliteLangตอนนี้มี int/boolจึงใช้ GPRsเท่านั้น.

## 23. Calling Convention Constraints

Allocatorต้องรู้ precolored/fixed registers:
- args registers
- RAX return
- RAX/RDX for IDIV
- caller/callee-saved classes

Instruction constraintsมีผลต่อ allocation/coalescing.

## 24. Callee-Saved Strategy

Backend baselineไม่ใช้ RBX/R12–R15สำหรับ temps จึงไม่ต้อง save. Allocator future versionถ้าใช้ ต้อง emit prologue/epilogue saves.

## 25. Peephole Optimization

หลัง codegenอาจลบ redundant movesหรือ combine patterns แต่ต้อง preserve flags/control behavior.

## 26. Branch Lowering

IR comparison materialize boolก่อน branchใน baseline. Optimized backendอาจ fuse:
```text
cmp + setcc + test + jne
```
เป็น `cmp + jcc` เมื่อ usesอนุญาต.

## 27. Machine IR

Production compilersมักมี target-specific machine IRก่อน final encodingเพื่อ model implicit operands, register classes, scheduling.

## 28. Assembly vs Direct Encoding

Course emits GNU assemblyเพื่อให้ inspectได้และ reuse assembler/linker. Direct machine-code emissionต้อง implement encodings/relocationsเอง.

## 29. Object Emission

Chapter 12อาจเชื่อม backendกับ object generation/toolchain pipeline. ตอนนี้ GCC/Clang driver assemble/link generated `.s`.

## 30. Correctness Tests

Backend testsควรครอบ:
- constants/arithmetic
- signed comparisons
- if/while
- short circuit
- calls
- recursion
- 0–8+ args
- division/modulo
- negative values
- frontend errors

## 31. Differential Testing

แนวทางต่อยอด: interpreter IRเป็น reference แล้ว compareกับ compiled executableหลาย generated programs.

## 32. Optimization Boundary

`--opt` ใช้ local IR optimization Chapter 10ก่อน codegen. Correctnessต้องเหมือน non-optimized build.

## 33. ABI + ELF Verification

ใช้:
```bash
objdump -d -Mintel
readelf -h
readelf -s
```
เพื่อเชื่อม compiler backendกับ Chapters 03–07.

## 34. Debugging Generated Code

ใช้ `gdb`, break function, inspect frame/args. ตอนนี้ compilerยังไม่ emit DWARF source maps จึงเป็น assembly-level debugging.

## 35. Backend Checklist

IR semantics? widths/signedness? stack layout? alignment? call clobbers? fixed regs? branch targets? division constraints? frame cleanup? generated assembly accepted? runtime result correct?

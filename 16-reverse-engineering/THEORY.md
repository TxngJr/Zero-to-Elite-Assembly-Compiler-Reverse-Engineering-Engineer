# Theory — Reverse Engineering

## 1. Reverse Engineering as Evidence Work

Reverse engineeringคือการ infer structure/behaviorจาก artifacts. สิ่งสำคัญคือแยก:

- **fact** — เห็นโดยตรงจาก ELF/disassembly/runtime state
- **inference** — interpretationที่ evidenceสนับสนุน
- **unknown** — ยังพิสูจน์ไม่ได้

อย่าตั้งชื่อ functionว่า `decrypt_password` เพียงเพราะมัน XOR bytes.

## 2. Provenance First

ก่อนวิเคราะห์:
- source/provenance
- hash
- file size
- build contextถ้ารู้

Course labใช้ binariesที่ buildเองเสมอ.

## 3. Static vs Dynamic Analysis

Static:
- file/readelf/nm/objdump/strings
- ไม่ execute target

Dynamic:
- run under debugger
- observe actual paths/registers/memory

ใช้ทั้งสองเพื่อ cross-checkกัน.

## 4. ELF Triage

เริ่ม:

```bash
file target
readelf -hW target
readelf -lW target
readelf -SW target
readelf -sW target
readelf -rW target
readelf -dW target
```

ถาม:
- PIE?
- interpreter?
- stripped?
- dynamic dependencies?
- executable segments?
- debug info?

## 5. Symbols

Symbolsช่วย function discoveryอย่างมาก แต่ stripped binaryอาจเหลือ dynamic symbolsหรือไม่มี local names.

ชื่อ symbolเป็น metadata—not proofว่า functionทำตามชื่อจริงทุกอย่าง.

## 6. Disassembly

```bash
objdump -d -Mintel target
```

อ่าน instructionตาม:
- operand width
- memory addressing
- flag producer/consumer
- branches/calls
- ABI registers

## 7. Function Boundaries

เมื่อไม่มี symbols heuristicsอาจดู:
- call targets
- alignment
- prologue/epilogue patterns
- control-flow reachability
- unwind info
- relocation references

ไม่มี heuristicเดียว perfect.

## 8. Compiler Fingerprints — Use Carefully

Code patternsเปลี่ยนตาม compiler/version/options. อย่าระบุ compilerจาก one instruction sequenceด้วยความมั่นใจเกิน evidence.

## 9. O0 vs O2

O0:
- stack localsมาก
- source-like control flow
- frame pointerมักเห็น

O2:
- inlining
- constant propagation
- register allocation
- branch simplification
- vectorizationบางกรณี
- tail calls

ดังนั้น functionจาก sourceอาจหายหรือ merge.

## 10. PIE / ASLR

PIE disassembly addressesเป็น image-relative link-time addresses. Runtime baseเปลี่ยนได้เพราะ ASLR.

ใช้ debugger mappingsเพื่อแปลง runtime↔image address.

## 11. RIP-relative Data

Pattern:

```asm
lea rdi, [rip + displacement]
```

มักชี้ static data/string/table. คำนวณ targetจาก next RIP + signed displacement.

## 12. Constants

Immediate constantsอาจเป็น:
- masks
- sizes
- enum values
- loop bounds
- addresses (non-PIE cases)

อย่าตั้ง semantic meaningจน cross-reference uses.

## 13. Strings

Stringsช่วย anchor behavior แต่:
- dead stringsอาจเหลือ
- encoded/compressed dataไม่ปรากฏ
- localizationเปลี่ยน wording

String presenceไม่พิสูจน์ pathถูก execute.

## 14. Cross References

ถาม “ใครอ้าง string/table/functionนี้?” แล้ว follow code/data references.

## 15. Switch Statements

O0อาจ chain comparisons. O2อาจใช้:
- jump table
- lookup table
- arithmetic formula
- balanced branches

source `switch`ไม่ได้ guarantee jump table.

## 16. Loops

Recognize:
- induction variable
- condition/back edge
- array stride
- accumulator
- exit conditions

Optimized loopsอาจ unroll/vectorize.

## 17. Arrays

Addressing `base + index*4` บอก element stride 4 bytesได้ แต่ไม่ได้บอก source typeชื่ออะไรแน่นอน.

## 18. Struct Recovery

Repeated accessesเช่น:
```text
[base+0]
[base+8]
[base+16]
```
suggest fields/array layout.

Padding/alignment/inheritance/unionทำให้ reconstructionมี uncertainty.

## 19. Signedness

Signed/unsigned often inferredจาก:
- `jl/jg` vs `jb/ja`
- `movsx` vs `movzx`
- `idiv` vs `div`

แต่ optimized codeอาจ transform comparisons.

## 20. Return Values / Calls

SysV ABIช่วย identify:
- args in RDI, RSI, RDX, RCX, R8, R9
- return in RAX
- stack argsหลังหก integer args

แต่ type width/aggregate classificationต้องดู instructions/context.

## 21. Indirect Calls

`call rax` หรือ `call [mem]`อาจเป็น:
- function pointer
- virtual dispatch
- callback table
- PLT/GOT indirection

ต้อง trace source of target.

## 22. Dynamic Linking Noise

PLT, GOT, startup/runtime functionsสร้าง codeที่ไม่ใช่ application logic. Chapter 07ช่วยแยก layerเหล่านี้.

## 23. C++ Preview

C++เพิ่ม:
- name mangling
- vtables
- constructors/destructors
- RTTI
- exceptions

Course challenge suiteเน้น Cก่อนเพื่อแยก core RE skills.

## 24. GDB Workflow

กับ course binary:

```text
start / starti
break function or *address
disassemble /r
info registers
x/...
si / ni
bt
info proc mappings
```

เขียน predictionก่อน step.

## 25. Dynamic Observation Is Path-Specific

การรัน inputหนึ่งเห็น pathหนึ่ง ไม่พิสูจน์ว่า functionไม่มี branchesอื่น.

## 26. CFG

Control-flow graphช่วย:
- enumerate blocks
- identify loops
- locate joins
- reason unreachable paths

`cfg_extract.py`ในบทนี้ใช้ objdump textอย่างง่ายและไม่แทน disassembler frameworkระดับ production.

## 27. Data-Flow

Track:
- definitions
- uses
- register overwrites
- memory aliases
- call clobbers

ตั้งชื่อ symbolic valuesของตัวเองช่วยลด cognitive load.

## 28. Calling Context

Function behaviorอาจเข้าใจได้จาก callersเร็วกว่าดู functionเดี่ยว. Callerบอก argument meaning/expected return.

## 29. Callee Context

Calleesที่ functionเรียกให้ cluesเช่น allocation, formatting, I/O แต่ library call nameไม่ได้อธิบาย full behavior.

## 30. Stripped Binary

Stripอาจลบ:
- local symbols
- debug info

แต่ machine code, dynamic metadata, unwind infoและบาง exported symbolsยังอยู่ตาม build.

## 31. Static Libraries

Static-linked library codeอาจดูเหมือน app code. Signatures/flirt-style matchingเป็น advanced topic; courseไม่ใช้ proprietary signature databases.

## 32. Compiler-Generated Code

Stack canary, CET, sanitizer instrumentation, PLT stubs, profiling hooksอาจแทรก code. ต้องเรียนรู้ build flagsก่อนสรุป logic.

## 33. Security Hardening Indicators

Static inspectionสามารถดู:
- PIE
- NX/GNU_STACK
- RELRO
- stack protector references

นี่เป็น posture metadata ไม่ใช่ proofว่า binary “secure”.

## 34. Pseudocode

Good pseudocode:
- preserve conditions/types uncertainty
- use meaningful but tentative names
- avoid inventing APIs
- cite assembly evidenceใน notes

## 35. Hypothesis Testing

ตัวอย่าง:
1. infer function sums int array
2. set breakpoint
3. inspect RDI/RSI
4. step loop
5. verify stride/accumulator
6. test another input

## 36. Binary Diffing

Compare O0/O2หรือ versions:
- symbols
- section sizes
- function disassembly
- control-flow shapes

Address-only diffเปราะเพราะ layout changes.

## 37. Patch Analysis

Defensive patch analysisถาม:
- functionไหนเปลี่ยน
- condition/length checkอะไรเพิ่ม
- data-flowเปลี่ยนอย่างไร
- regression testอะไรควรมี

บท 17ใช้แนวคิดนี้กับ course parser bug.

## 38. Reporting

RE reportควรมี:
- target provenance/hash/build variant
- tools/commands
- observations
- reconstructed logic
- confidence
- unresolved questions
- screenshots/log snippetsเมื่อจำเป็น

## 39. Ethics / Authorization

มีความสามารถอ่าน binaryไม่ได้แปลว่ามีสิทธิ์วิเคราะห์ทุก target. ตรวจ license/authorizationและขอบเขตเสมอ.

## 40. Mental Checklist

provenance? ELF? symbols? strings? functions? CFG? data references? ABI? optimization? runtime mappings? evidence vs inference? confidence?

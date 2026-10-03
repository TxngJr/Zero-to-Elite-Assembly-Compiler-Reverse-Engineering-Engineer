# Objectives

เมื่อจบบทนี้ควรสามารถ:
- อธิบาย instruction selection
- map IR arithmetic/comparisons/control flowไป x86-64
- สร้าง stack frameและ stack slots
- lower function parameters/returnsตาม SysV AMD64 ABI
- รองรับ arguments > 6 ผ่าน caller stack
- รักษา 16-byte alignmentก่อน call
- emit signed divisionด้วย `cqo/idiv`
- emit comparisonsด้วย `cmp/setcc`
- lower short-circuit CFGเป็น labels/jumps
- compile recursionและ loops
- อธิบาย virtual registers, spilling, liveness และ register allocation
- อธิบาย linear scan vs graph coloring
- แยก codegen correctnessจาก code quality/optimization
- inspect generated assembly/ELFด้วย objdump

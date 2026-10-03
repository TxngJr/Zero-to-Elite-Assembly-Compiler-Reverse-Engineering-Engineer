# Labs

1. Compile `return42.el` แล้ว annotateทุก assembly line.
2. คำนวณ frame size/slot offsetsของ main.
3. Trace signed comparison lowering.
4. Trace while CFG→labels.
5. Trace `&&` short-circuitและพิสูจน์ `boom()`ไม่ถูก call.
6. Trace recursive `fact` frames.
7. Trace `sum8`: args 1–6 registers, 7–8 stack.
8. เปลี่ยนเป็น 7 argsและตรวจ paddingก่อน call.
9. เพิ่ม signed division/modulo program.
10. objdump generated executable; match source function symbols.
11. run GCC vs Clang assembler/linker path.
12. compare `--opt` vs baseline assembly.
13. วาด live intervalsสำหรับ simple expression.
14. ทำ manual allocationของ 3 virtual valuesลง RAX/RCX/RDX.
15. เพิ่ม peephole passเล็ก ๆโดยมี regression tests.

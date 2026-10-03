# Common Mistakes

- IR temp = physical register
- codegenถูกแล้วต้องเร็ว
- spill = compiler failure
- ลืม 16-byte alignmentก่อน call
- push stack argsผิดลำดับ
- arg7 offsetผิดหลัง prologue
- divisionไม่เตรียม RDX:RAX
- ใช้ unsigned jccกับ signed language int
- caller-saved valuesคาดว่าจะรอด call
- allocatorใช้ callee-savedแต่ไม่ restore
- short-circuit compileเป็น bitwise op
- generated assembly assembleผ่าน = semanticsถูก

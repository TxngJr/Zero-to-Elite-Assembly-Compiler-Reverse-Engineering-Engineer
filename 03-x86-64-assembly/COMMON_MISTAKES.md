# Common Mistakes

- เขียน EAX แล้วคิด upper RAXคงเดิม
- `[rax]` คือค่าใน RAX แทนที่จะเป็น dereference
- `lea` อ่าน memory
- ใช้ signed/unsigned jccสลับกัน
- คิดว่า CMPเองเลือก signedness
- สมมติทุก instructionรับ memory-to-memory
- ไม่ระบุ operand sizeเมื่อ inferไม่ได้
- คิดว่า XOR-zeroเหมือน MOV-zeroทุก flag effect
- push/popแล้วไม่ restore stack
- คิดว่า CALLกำหนด argument registers
- คิดว่า assembler directiveเป็น CPU instruction
- อ่าน disassemblyโดยไม่สน operand width

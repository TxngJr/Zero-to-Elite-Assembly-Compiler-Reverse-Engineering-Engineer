# Answers and Hints

- 4 page directories × 512 entries × 2 MiB = 4 GiB.
- Multiboot2 headerต้องอยู่ within first 32768 bytesและ alignedตาม protocol.
- PMM reserveอย่างน้อย kernel image + boot informationก่อนแจก frames.
- IRQ handlerต้อง EOI PICก่อนกลับ.
- Stack-slot/heap memoryไม่เท่ากับ physical frame ownership.
- Chapter14ยัง ring0-only; process isolationต้อง user mode + page tables + schedulerใน Chapter15.

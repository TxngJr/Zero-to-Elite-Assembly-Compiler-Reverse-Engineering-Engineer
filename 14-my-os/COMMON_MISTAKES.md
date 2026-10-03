# Common Mistakes

- ใช้ normal libcใน freestanding kernel
- ลืม `-mno-red-zone`
- Multiboot headerอยู่นอก first 32 KiB
- page tablesไม่ aligned 4 KiB
- CR3โหลด virtualแทน physical address
- enable pagingก่อน tables/GDTพร้อม
- IRQ handlerลืม EOI
- generic ISR `iretq` โดยไม่สน error-code frame
- PMMแจก memoryที่ทับ kernel/boot info
- heap allocatorกับ frame allocatorปนกัน
- keyboard ISRทำงานหนักเกินไป
- QEMU bootผ่านแล้วเรียก production-ready OS

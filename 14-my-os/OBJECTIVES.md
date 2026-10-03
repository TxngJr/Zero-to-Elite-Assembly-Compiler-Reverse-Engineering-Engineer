# Objectives

เมื่อจบบทนี้ควรสามารถ:

- build/link freestanding ELF64 kernel
- อธิบาย Multiboot2 headerและ boot info pointer
- อ่าน 32-bit early-boot assembly
- สร้าง page tablesด้วย 2 MiB identity mappings
- enable PAE/long mode/pagingและ far jumpเข้า 64-bit code
- ใช้ linker scriptจัด kernel sections
- initialize serial/VGA console
- build/load IDT
- remap legacy PICและ handle IRQ0/IRQ1
- configure PIT timer
- อ่าน PS/2 keyboard scan codes subset
- parse Multiboot2 memory map
- reserve kernel/boot-info memory
- allocate physical 4 KiB framesแบบ bump
- implement kernel bump heap
- ใช้ `hlt` idle loopกับ interrupts
- inspect kernel ELFด้วย readelf/nm/objdump
- boot kernelด้วย GRUB/QEMUเมื่อ toolingพร้อม
- อธิบาย limitationsของ early kernelโดยไม่เรียกมัน production OS

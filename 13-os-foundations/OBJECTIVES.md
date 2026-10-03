# Objectives

เมื่อจบบทนี้ควรสามารถ:

- อธิบาย boot chain จาก firmware → bootloader → kernel entry
- แยก BIOS/UEFI conceptออกจาก Multiboot2 boot protocol
- อธิบาย protected modeและ long mode transition
- อธิบาย CR0/CR3/CR4 และ EFER rolesระดับ concept
- อ่าน GDT/IDT descriptor layouts
- อธิบาย privilege rings/CPL/DPL/RPLระดับพื้นฐาน
- อธิบาย interrupt gate, exception, IRQ และ `iretq`
- แยก PIC/PIT/APIC concepts
- อธิบาย port I/O vs MMIO
- แยก physical/virtual addressและ 4-level x86-64 page-table indices
- ตรวจ canonical virtual addresses
- อธิบาย 4 KiB pages, 2 MiB huge pages, TLB และ page faults
- อธิบาย freestanding C constraints
- อธิบาย linker script/kernel sections
- วาง memory-management roadmap: frame allocator → page mapper → heap
- เข้าใจ kernel/user privilege transitionและ syscall boundaryภาพใหญ่

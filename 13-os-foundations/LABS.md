# Labs

1. วาด firmware→bootloader→kernel chain.
2. เปรียบเทียบ hosted `main` กับ freestanding entry.
3. เขียน long-mode transition checklistด้วยมือ.
4. Decode GDT code/data descriptor constants.
5. ใช้ descriptor-lab inspect 16-byte IDT gate.
6. แยก interrupt gate fields.
7. วาด exception vs IRQ flow.
8. อธิบาย PIC remap 0x20/0x28.
9. คำนวณ PIT divisorสำหรับ 100 Hz.
10. ใช้ page-walk-sim split virtual address.
11. คำนวณ PML4/PDPT/PD/PT indicesด้วยมือ.
12. ทดสอบ canonical/non-canonical addresses.
13. Map two simulated pagesและลอง permissions.
14. วาด 2 MiB identity mapสำหรับ first 4 GiB.
15. ออกแบบ PMM reservationสำหรับ kernel + boot info.
16. วาง section layoutใน linker script.
17. เปรียบเทียบ VGA vs serial console.
18. อธิบาย `-ffreestanding -mno-red-zone`.
19. วาด ring3→kernel syscall transitionล่วงหน้า.
20. ก่อน Chapter14 เขียน boot-debug checklist.

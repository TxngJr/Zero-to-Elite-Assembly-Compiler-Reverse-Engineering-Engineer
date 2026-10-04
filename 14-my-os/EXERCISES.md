# Exercises — EliteOS64

## Response contract

ทุกข้อให้มี **Explain + Concrete example + Evidence + misconception/boundary**. ถ้าพูดถึง hardware state ให้ชี้ source/objdump/serial logที่พิสูจน์ claim.

## A. Boot / Long Mode

1. วาด GRUB Multiboot2 handoffถึง `_start`: EAX/EBXมีอะไร.
2. คำนวณ Multiboot2 header checksumและอธิบาย placement requirement.
3. อธิบายเหตุผลที่ early stackต้องสร้างเอง.
4. จาก `boot.s` เขียนลำดับ CR4.PAE → CR3 → EFER.LME → CR0.PG → far jump และบอกว่าถ้าสลับแต่ละคู่ผิดจะเสี่ยงอะไร.
5. คำนวณ 2048 × 2 MiB = 4 GiB mappingและชี้ PDE flags `0x83`.
6. ใช้ `objdump`หา `wrmsr`, CR3 loadและ far transfer evidence.
7. อธิบายทำไม kernel ELF64ยังมี 32-bit early codeได้.

## B. Console / Interrupts

8. Trace `console_putc`หนึ่ง byteไป COM1และ VGA.
9. Trace serial input byteจาก COM1 LSR→`console_try_read`→`shell_feed_char`.
10. วาด 16-byte IDT gateของ IRQ0 handler.
11. อธิบาย PIC remap 0x20/0x28และทำไม IRQ vectorsไม่ควรชน CPU exceptions.
12. คำนวณ PIT divisorสำหรับ 100 Hzจาก 1193182 Hz.
13. อธิบาย EOIและผลถ้าลืมส่ง.
14. เปรียบเทียบ IRQ0 stubกับ IRQ1 stub: stateไหนถูกอ่าน/แก้.
15. อธิบายทำไม `timer_ticks >= 3` ทำให้ QEMU gateเป็น runtime proofมากกว่า static grep.

## C. Exception Diagnostics

16. วาด stack frameของ #UD (ไม่มี error code) และ #PF (มี error code) ก่อน `exception_common`.
17. อธิบาย synthetic zeroใน no-error stub.
18. อธิบาย CR2มีความหมายเฉพาะ page faultอย่างไร.
19. อธิบายว่าทำไม current panic handler `noreturn` ทำให้ destructive stack realignmentยอมรับได้.
20. เสนอ normalized full frameที่เก็บ general registers + RIP/CS/RFLAGS/RSP/SS.
21. อธิบาย IST/TSSจะช่วย double faultอย่างไร.

## D. Physical Memory / Heap

22. Trace Multiboot memory-map tag parserพร้อม alignment 8 bytes.
23. อธิบาย `safe_start=max(kernel_end,boot_info_end)`.
24. ให้ memory regionตัวอย่างแล้วคำนวณ first frameที่ allocatorแจก.
25. รัน shell `alloc`สองครั้งและยืนยัน addressต่าง 0x1000.
26. อธิบาย limitation: allocatorใช้ usable rangeแรกและไม่มี free.
27. แยก PMM vs VMM vs heapด้วยคำถาม “ใครจัดอะไร”.

## E. Runtime / QEMU Evidence

28. รัน `make -C 14-my-os qemu-test`; แนบ serial log.
29. พิสูจน์ marker order: console → PMM → IDT/PIT config → PIT IRQ → shell ready.
30. พิสูจน์ serial shell inputจริงด้วย `ticks=` ใน log.
31. รัน interactive `help,ticks,mem,alloc` และบันทึกผล.
32. intentionally breakหนึ่ง milestoneใน local copy, ทำนาย first missing marker, แล้วคืน fix.
33. อธิบายสิ่งที่ QEMU passยังไม่พิสูจน์เกี่ยวกับ hardwareจริง.

## F. Next-step Design

34. เขียน patch series: robust exceptions → bitmap PMM → 4K mapper → TSS → ring3.
35. ระบุ invariants/testsที่ต้องผ่านหลังแต่ละ patchเพื่อรักษา known-good boot.

## Practical submission

ต้องมี kernel static evidence, QEMU serial runtime evidence, exception-frame drawing, memory allocation calculation และ local patch/testหนึ่งชิ้น.

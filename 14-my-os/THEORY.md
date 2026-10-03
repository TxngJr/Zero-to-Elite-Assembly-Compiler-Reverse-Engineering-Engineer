# Theory — EliteOS64

## 1. Kernel Artifact

EliteOS64เป็น statically linked ELF64 executableที่ GRUBอ่านผ่าน Multiboot2.

เราไม่ได้ copy Linux kernel architecture; เป้าหมายคือ minimal educational kernelที่เชื่อมความรู้ Chapters 00–13.

## 2. Link Address

Linker scriptวาง Multiboot headerที่ 1 MiBและ codeหลัง alignment:

```text
0x00100000  .multiboot
0x00101000  .text
...
```

`kernel_end`เป็น linker-defined symbolให้ PMM reserve image.

## 3. Why Multiboot2

เขียน BIOS/UEFI disk/filesystem loaderเองจะกลบเนื้อหา kernel. GRUBให้ boot protocolที่ stableพอสำหรับ learning.

## 4. Early 32-bit Entry

GRUB Multiboot2 x86 handoffเริ่มที่ `_start`ใน protected modeและส่ง:
- EAX = Multiboot2 boot magic
- EBX = physical pointer to Multiboot information

boot codeเก็บสองค่านี้ก่อนเปลี่ยน mode.

## 5. Early Stack

Kernelเตรียม 16 KiB stackใน `.bss`. ไม่มี process/runtimeสร้าง stackให้เรา.

## 6. Early Page Tables

Implementationสร้าง:
- one PML4
- one PDPT
- four page directories

แต่ละ PDมี 512 × 2 MiB entries → 1 GiB.
4 PDs → identity-map first 4 GiB.

## 7. Why 4 GiB Mapping

Multiboot boot dataใช้ 32-bit physical pointer. Mapping first 4 GiBทำให้ kernelเข้าถึง early boot structures/device legacy addressesง่ายใน learning model.

นี่ไม่ใช่ long-term virtual-memory design.

## 8. Page Entry

Early huge-page entryใช้ flags:
- Present
- Writable
- Page Size

Physical baseมาจาก index × 2 MiB.

## 9. Entering Long Mode

boot sequence:

```text
CR4.PAE=1
CR3=PML4
EFER.LME=1
CR0.PG=1
LGDT
far jump to 64-bit code selector
```

Far jump encoded explicitlyเพื่อให้ GNU assemblerและ Clang integrated assemblerรับ sourceเดียวกัน.

## 10. 64-bit Entry

หลัง long-mode jump:
- load data selectors
- set RSP
- clear RBP
- move boot magic/info into SysV args
- call `kernel_main`

จากจุดนี้เราใช้ C ABIภายใน kernelเอง.

## 11. Kernel C Flags

สำคัญ:

```text
-ffreestanding
-fno-stack-protector
-fno-pic -fno-pie
-mno-red-zone
-mcmodel=kernel
-mno-sse -mno-sse2 -mno-mmx -mno-80387
```

ช่วงแรกหลีกเลี่ยง floating/SIMD stateก่อน initialize CPU facilities.

## 12. Serial Console

COM1 base `0x3F8`. Kernel initialize baud/divisor/line/FIFO/modem settingsแล้ว poll transmitter-ready.

Serialเป็น primary debugging evidenceเมื่อ boot failureไม่มี UI.

## 13. VGA Console

`0xB8000` legacy text bufferเก็บ 16-bit cells:
- low byte character
- high byte attribute

Console implementationมี newline/backspace/scroll.

## 14. IDT

C codeสร้าง 256 IDT gates:
- default gate → halt handler
- vector 32 → timer IRQ
- vector 33 → keyboard IRQ

`lidt`โหลด IDTR.

## 15. Why Default Handler Halts

Exception frame layoutsต่างกันเพราะบาง vectors push error code. Chapter 14 default handlerจึง haltแทน returnผ่าน generic incorrect frame.

Robust exception frameworkเป็น Chapter 15 challenge.

## 16. IRQ Stubs

Timer/keyboard stubsเขียน assemblyเล็กเพื่อ:
- preserve RAX
- update shared state/read port
- send PIC EOI
- `iretq`

ไม่ได้ call Cจาก interrupt context จึงหลีกเลี่ยง stack-alignment/register-save complexityใน milestoneแรก.

## 17. PIC

Master/slave PICถูก remapเป็น vectors 32/40. หลัง setupเรา unmask IRQ0/IRQ1เท่านั้น.

## 18. PIT

PIT channel 0 configured periodic modeที่ ~100 Hz.

`timer_ticks` incrementใน IRQ0.

## 19. Keyboard

IRQ1อ่าน one-byte set-1 scancodeจาก port `0x60`.

Main loopconsume `last_scancode`. Translatorรองรับ lowercase/basic keys subset; ไม่มี Shift/Ctrl/extended sequences.

## 20. Deferred Work

ISRทำงานสั้น:
```text
IRQ → capture state → EOI → iretq
```

Main loopทำ shell processing. นี่เป็น early formของ interrupt top-half vs deferred-work thinking.

## 21. Multiboot Tags

Boot info:
```text
total_size
reserved
tag
tag
...
end tag
```

Tags align 8 bytes.

Memory-map tag type 6ประกอบ entriesที่มี address/length/type.

## 22. PMM

PMMรุ่นนี้:
1. อ่าน usable memory entry
2. reserve everythingก่อน max(kernel_end, end of boot info)
3. cap allocatorที่ first 4 GiBเพราะ early identity map
4. align 4 KiB
5. bump `next_frame`

ไม่มี free/reuse.

## 23. Why Reserve Boot Info

ถ้า allocatorแจก frameที่ยังเก็บ Multiboot tags เราจะ overwrite memory mapที่กำลังใช้งาน.

## 24. Heap

64 KiB static heapใน BSS:
- 16-byte alignment
- bump pointer
- no free

นี่แยก variable-size allocation conceptจาก physical framesก่อนมี VMMเต็ม.

## 25. Shell

Commands:
- `help`
- `ticks`
- `mem`
- `alloc`
- `clear`

`alloc`ขอ physical frameเพื่อให้เห็น PMMทำงานจริง.

## 26. Idle Loop

```text
sti
loop:
  hlt
  consume keyboard event
```

Timer/keyboard interruptsปลุก CPUจาก HLT.

## 27. Build Validation Without QEMU

`make test` ตรวจ:
- ELF64 x86-64
- Multiboot magicอยู่ first 32 KiB
- header checksum
- required sections/symbols
- long-mode instructions
- IDT/interrupt instructions

จึงตรวจ image mechanicsได้แม้ CIไม่มี virtualization.

## 28. Boot Validation With QEMU

`make qemu-test`:
- build GRUB ISO
- boot QEMU under timeout
- capture serial log
- verify `EliteOS64 booted`

QEMU smoke testไม่ได้พิสูจน์ physical-hardware compatibility.

## 29. Current Memory Model

Kernel, VGA, boot infoและ allocated framesใช้ identity addresses. ยังไม่มี higher-half kernel, NX/W^X policy, per-process spacesหรือ frame reuse.

## 30. Current Interrupt Model

Legacy PIC/PIT/PS2เหมาะกับ PC emulator. Advanced chapterจะเพิ่ม robust exception frames/APIC conceptsและ synchronization.

## 31. Current Security Boundary

ยังไม่มี user mode จึงทุก codeอยู่ ring0. นี่เป็นเหตุผลที่ Chapter 14ยังไม่ใช่ multi-process OS.

## 32. Debug Strategy

ถ้า bootไม่ถึง serial:
- inspect Multiboot header
- inspect entry
- inspect linker VMAs
- inspect long-mode setup

ถ้า serialเริ่มแล้ว crash:
- narrow stageด้วย serial checkpoints
- QEMU `-d int,cpu_reset`เมื่อจำเป็น
- GDB remote stubเป็น Chapter 15 extension.

## 33. Milestone Discipline

เพิ่ม subsystemทีละชั้นและรักษา known-good boot. Kernel bugsก่อน consoleพร้อมยากกว่าปกติหลายเท่า.

## 34. Next Chapter

Chapter 15ควรต่อ:
VMM 4 KiB mapper → robust exception frames → TSS/user mode → processes/context switch → scheduler → syscalls → VFS/filesystem → SMP/synchronization.

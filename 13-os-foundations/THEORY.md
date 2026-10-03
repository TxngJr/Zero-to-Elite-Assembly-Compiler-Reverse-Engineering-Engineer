# Theory — OS Foundations

## 1. Hosted vs Freestanding

Normal C programอยู่ใน hosted environment:

```text
_start → C runtime → main → libc → syscalls
```

Kernelเป็น freestanding program. มันไม่มี guaranteeว่าจะมี libc, process loaderหรือ user-space stack layout.

Compiler flag `-ffreestanding` บอก compilerว่า environmentไม่ใช่ hosted C implementationเต็มรูปแบบ.

## 2. Boot Chain

Simplified:

```text
Firmware
  ↓
Bootloader
  ↓
Kernel image
  ↓
Kernel entry
```

Bootloaderช่วยอ่าน filesystem/load kernelและส่ง boot information.

## 3. BIOS vs UEFI

BIOS bootแบบ legacyเริ่มจาก firmware interfacesเก่าและ real-mode conventions. UEFIเป็น firmware environmentสมัยใหม่ที่โหลด EFI applications.

Chapter 14ใช้ GRUB + Multiboot2 เพื่อหลีกเลี่ยงการเขียน filesystem/firmware loaderเองตั้งแต่วันแรก.

## 4. Multiboot2

Multiboot2เป็น bootloader↔kernel contract.

Kernelวาง header magicในช่วงต้นของ image. Bootloaderส่ง:
- magic value
- pointerไป boot information tags
- memory mapและข้อมูลอื่นตาม tags

บน x86 Multiboot2 handoffเริ่มใน 32-bit protected-mode environment; kernelของเราจะเปิด long modeเอง.

## 5. x86 Modes

Historical model:

```text
real mode → protected mode → long mode
```

Modern bootloaderอาจจัดบางส่วนให้แล้ว แต่ kernelต้องรู้ mode contractของ protocolที่ใช้.

## 6. Long Mode Requirements

Simplified transition:
1. page tablesพร้อม
2. CR4.PAE = 1
3. CR3 = PML4 physical address
4. EFER.LME = 1
5. CR0.PG = 1
6. load 64-bit code segment
7. far control transferเข้า 64-bit code

Orderและdescriptor correctnessสำคัญมาก.

## 7. Control Registers

- CR0: paging/protection/control bits
- CR2: faulting linear addressหลัง page fault
- CR3: top-level page-table physical address
- CR4: architecture features เช่น PAE

Privileged instructionsใช้ได้เฉพาะ kernel/appropriate privilege.

## 8. EFER

IA32_EFERเป็น model-specific register. LME enable long mode; NXEเกี่ยวกับ execute-disableเมื่อรองรับ/เปิด.

MSRsอ่าน/เขียนผ่าน `rdmsr/wrmsr`.

## 9. GDT

Global Descriptor Tableยังจำเป็นใน long modeแม้ segmentationส่วนใหญ่ flat/ignored.

เราต้องมีอย่างน้อย:
- null descriptor
- 64-bit kernel code descriptor
- data descriptor

ต่อไป user modeต้องเพิ่ม user code/dataและ TSS.

## 10. Privilege Rings

x86มี rings 0–3. OSทั่วไปใช้:
- ring 0 kernel
- ring 3 user

Hardwareตรวจ privilegeผ่าน segment selectors/gates/page permissions.

## 11. TSS Preview

Task State Segmentใน x86-64ไม่ได้ใช้ hardware task switchingแบบเดิมเป็นหลัก แต่เก็บ privileged stack pointersและ Interrupt Stack Table.

สำคัญเมื่อเข้าสู่ user modeหรือรับ critical exceptionsบน dedicated stack.

## 12. IDT

Interrupt Descriptor Tableมี 256 entries. x86-64 interrupt gateหนึ่ง entryมี handler address, selector, IST index, type/attributes.

`lidt` โหลด IDTR.

## 13. Exceptions

CPU exceptionsตัวอย่าง:
- #DE divide error
- #UD invalid opcode
- #GP general protection
- #PF page fault
- #DF double fault

บาง exceptions push error code, บางอันไม่ push. Generic ISR frameworkต้อง normalize stack frameอย่างระวัง.

## 14. Interrupts / IRQs

External hardware interruptมาจาก interrupt controller. Legacy PCมี 8259 PIC; modern machinesมี APIC/IOAPIC.

Chapter 14ใช้ PICใน QEMUเพื่อความเรียบง่ายก่อน Advanced OS.

## 15. PIC Remap

Legacy PIC default vectorsชน CPU exception range. Educational kernelsมัก remap:
- IRQ0–7 → vectors 32–39
- IRQ8–15 → vectors 40–47

หลัง handlerต้องส่ง EOI.

## 16. PIT

Programmable Interval Timerเป็น legacy timerที่ QEMUจำลองง่าย. ตั้ง divisorจาก base frequencyเพื่อสร้าง periodic IRQ0.

Modern OSใช้ APIC timers/HPET/TSC-based mechanismsด้วย.

## 17. Keyboard Controller

Classic PS/2 keyboard IRQ1อ่าน scan codeจาก port `0x60`. Real hardware/input stackซับซ้อนกว่านี้; Chapter 14รองรับ subsetเล็กเพื่อฝึก interrupt path.

## 18. Port I/O vs MMIO

x86มี:
- port-mapped I/O ผ่าน `in/out`
- memory-mapped I/O ผ่าน load/storeไป mapped device ranges

ทั้งคู่ต้องระวัง ordering/device semantics.

## 19. Page Tables

4-level x86-64 (without LA57):

```text
VA bits:
47..39 PML4 index
38..30 PDPT index
29..21 PD index
20..12 PT index
11..0  offset
```

แต่ละ index 9 bits → 512 entries.

## 20. Canonical Addresses

ใน 48-bit virtual-address mode bits 63..48ต้อง sign-extend bit47. Non-canonical addressก่อ faultก่อน normal translation.

## 21. 4 KiB vs Huge Pages

Normal 4 KiB:
PML4 → PDPT → PD → PT → frame

2 MiB huge page:
PML4 → PDPT → PD entry with PS bit → 2 MiB frame

Chapter 14 boot codeใช้ 2 MiB pagesเพื่อ identity-map early memoryด้วย tablesน้อยลง.

## 22. Page Entry Flags

Common concepts:
- Present
- Writable
- User
- Accessed/Dirty
- Page Size
- NX (with EFER.NXE)

Exact bit semanticsต้องอ้าง architecture manualเมื่อ implement featuresจริง.

## 23. Identity Mapping

Identity mappingคือ:

```text
virtual address == physical address
```

ง่ายสำหรับ early boot แต่ production kernelมักมี higher-half mappingและแยก address spaces.

## 24. Physical Memory Manager

PMMจัด physical frames:

```text
memory map → usable regions → reserve kernel/boot data → allocate/free frames
```

Chapter 14ใช้ first-fit bump frame allocatorก่อน bitmap/buddy allocator.

## 25. Virtual Memory Manager

VMM/page mapperสร้าง page-table mappingsและ permissions. PMMตอบ “frameไหนว่าง”; VMMตอบ “VAนี้ mapไป frameไหน”.

## 26. Kernel Heap

Heap allocatorอยู่เหนือ memory mapping/frame allocation. รุ่นแรกใช้ bump allocator; advanced allocatorต้อง free/reuse/coalesce.

## 27. Kernel Stack

Kernelต้องจัด stackเอง. Interrupt/user→kernel transitionยิ่งต้อง model stack ownership/privilege changeอย่างชัดเจน.

## 28. Linker Script

Kernel linker scriptกำหนด:
- load address
- entry symbol
- section order
- alignment
- special symbols เช่น `kernel_end`

นี่ต่างจาก normal user-space executableที่ system linker script/runtimeจัดรายละเอียดส่วนใหญ่.

## 29. Serial Console

COM1 serialเหมาะกับ kernel debuggingใน QEMU:

```text
kernel → outb → QEMU serial → terminal/log
```

Serialยังใช้ได้แม้ VGA/UIพัง.

## 30. VGA Text Mode

Legacy framebuffer `0xB8000` ใช้ character+attribute pairs. เป็น teaching output path ไม่ใช่ modern graphics stack.

## 31. Halting

`hlt`หยุด coreจน interruptถัดไปเมื่อ interrupts enabled. Idle loop:

```text
sti
loop:
  hlt
  handle deferred work
```

## 32. Race Awareness

Interrupt handlerกับ main kernel codeแชร์ stateแบบ asynchronous. `volatile`ช่วยบังคับ accessesบางอย่างแต่ไม่แทน synchronization/atomicsสำหรับ complex shared state.

## 33. Kernel C Restrictions

หลีกเลี่ยง:
- libc calls
- floating point/SIMDก่อน initialize state
- red zoneบน kernel stacks
- stack protectorที่ต้อง runtime supportถ้ายังไม่ provide

ใช้ `-mno-red-zone`, freestanding flagsและ explicit runtime helpers.

## 34. User Mode Preview

การเข้า ring3ต้องมี:
- user code/data selectors
- user page permissions
- kernel stackใน TSS
- controlled transition `iretq/sysret`
- syscall/interrupt ABI

Chapter 15ค่อยต่อยอด.

## 35. OS Foundation Checklist

boot contract? CPU mode? descriptors? paging? stack? console? interrupts? timer? input? physical memory? virtual mapping? heap? privilege boundary? debugging path?

# Worked Examples — My OS: EliteOS64

แยก **static image evidence** ออกจาก **runtime QEMU evidence** ตลอดบทนี้.

## Example 1 — Static kernel image vs runtime boot

**Goal:** รู้ว่า `make test` และ `make qemu-test` พิสูจน์คนละอย่าง.

**Command / action:**

```bash
make -C 14-my-os clean test
make -C 14-my-os qemu-test
cat 14-my-os/build/serial.log
```

**Prediction:** static testควรพิสูจน์ ELF/Multiboot/symbol/instruction presence; runtime gateต้องเห็น PIT interruptsเกิดจริง.

**Expected key evidenceใน serial log:**

```text
EliteOS64 booted
[BOOT] console ok
[BOOT] pmm/heap ok
[BOOT] idt/pic/pit configured
[BOOT] pit irq ok
[BOOT] shell ready (serial + ps2 input)
commands: help ticks mem alloc clear
elite>
```

ลำดับ prompt/markerอาจต่างเล็กน้อยตาม implementation แต่ `pit irq ok` ต้องเกิดจาก `timer_ticks >= 3` ไม่ใช่ static printก่อน enable interrupts.

**What may vary:** physical addresses/memory-map-derived frame count, QEMU/GRUB version.

**Explain:** kernel ELFที่ linkสำเร็จอาจยัง triple fault; QEMU runtimeเป็นอีก evidence layer.

**Modification:** ใน local copy comment `pit_init(100)` แล้วทำนายว่า qemu-testจะหยุดถึง markerไหน. คืน codeหลังทดลอง.

**Failure mode:** อย่าแก้หลาย subsystemพร้อมกัน; markerแรกที่หายคือ boundaryแรกที่ควร debug.

**Reflection:** QEMU runtime passยังไม่พิสูจน์ hardware compatibilityอะไรบ้าง?

---

## Example 2 — Headless serial shellจริง

**Goal:** พิสูจน์ว่า `-serial stdio -display none` รับ inputได้ ไม่ใช่แค่ output.

**Command / action:**

```bash
make -C 14-my-os qemu
```

เมื่อเห็น `elite> ` ให้พิมพ์:

```text
help
ticks
mem
alloc
```

**Expected key evidence:**
- `help` → `help ticks mem alloc clear`
- `ticks` → ค่าเพิ่มจาก PIT
- `mem` → frame count + heap usage
- `alloc` → physical frame address และครั้งถัดไปเพิ่ม 0x1000

**What may vary:** frame address/count.

**Explain:** COM1 LSR bit0บอก data-ready; `console_try_read()`อ่าน byteแล้วส่ง `shell_feed_char()`. PS/2 IRQ pathเป็น inputอีกทางหนึ่ง.

**Modification:** เปิด `kernel/kernel.c` แล้ววาด event loop: `hlt → IRQ wake → PS/2 consume → serial poll`.

**Failure mode:** ถ้าเห็น promptแต่พิมพ์ไม่ได้ ให้ยืนยันว่ากำลังใช้ kernelใหม่และ commandมี `-serial stdio`; อย่าคิดว่า serial stdinคือ PS/2.

**Reflection:** ทำไม polling serialหลัง `hlt`ยังทำงานได้เมื่อ PIT interruptปลุก CPUเป็นระยะ?

---

## Example 3 — Exception diagnostics

**Goal:** เข้าใจ normalized exception frameและสิ่งที่ panic reportพิสูจน์.

**Command / action:**

```bash
objdump -d -Mintel 14-my-os/build/kernel.elf \
  | sed -n '/<exception_pf_stub>/,/<irq0_stub>/p'

grep -n -E 'exception_(de|ud|gp|pf)_stub|exception_panic|set_gate\(' \
  14-my-os/kernel/interrupts.c \
  14-my-os/kernel/interrupts.s
```

**Prediction:** #PF hardware push error codeอยู่แล้ว; stubจึง push vectorอย่างเดียว. #DE/#UDไม่มี hardware error code; stubต้อง push synthetic 0 + vector.

**Expected key evidence:** C handlerรับ `vector,error_code,rip`; page faultอ่าน CR2และ printก่อน halt.

**What may vary:** handler addresses.

**Explain:** generic `iretq` จาก unknown exception frameไม่ปลอดภัยถ้าเราไม่ normalize error-code layout; current diagnostic handlers intentionally never return.

**Modification:** วาด stack layoutของ #UDและ #PFที่ entry `exception_common`.

**Failure mode:** ถ้า stack alignmentถูกปรับ destructivelyแล้ว handlerจะ returnไม่ได้—current designใช้ `noreturn`จึงตรง contract.

**Reflection:** robust frameworkถัดไปควรเพิ่ม saved registers, CS/RFLAGS/RSP/SS, IST/TSS และ recoverability policyอย่างไร?

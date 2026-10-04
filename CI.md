# Continuous Integration

Repository นี้แยก verification ออกเป็น 3 ระดับเพื่อไม่ใช้คำว่า “verified” กว้างเกินหลักฐาน.

## 1. Full course repository checks

GitHub Actions รันทั้ง GCC และ Clang:

```bash
./scripts/verify-chapters.sh
```

สิ่งนี้ตรวจ source/build/tests ของ Chapters 00–18 แต่ **ไม่เท่ากับพิสูจน์ความเข้าใจของผู้เรียน**.

## 2. EliteOS64 runtime boot gate

CI ติดตั้ง QEMU + GRUB และรัน:

```bash
make -C 14-my-os qemu-test
```

gate นี้ต้องเห็น serial milestones:

```text
[BOOT] console ok
[BOOT] pmm/heap ok
[BOOT] idt/pic/pit configured
[BOOT] pit irq ok
[BOOT] shell ready (serial + ps2 input)
elite>
```

ดังนั้น OS runtime gate พิสูจน์มากกว่าการมี symbol/instruction อยู่ใน ELF: PIT IRQ ต้องเกิดจริงก่อน test ผ่าน.

## 3. Defensive diagnostics

CI แยก fixed regression tests ออกจาก intentionally injected defects:

```bash
make -C 17-security-lab test
make -C 17-security-lab sanitizer-demo
make -C 17-security-lab fuzz
```

- default tests ใช้ fixed code
- sanitizer-demo ตั้งใจสร้าง course-only defect และต้องถูก ASan จับ
- fuzz ใช้ Clang libFuzzer กับ parser ที่แก้แล้ว

## Claims policy

ข้อความที่เหมาะสม:

> Automated repository checks passed.

ไม่ควรแปลผลเป็น:

> ทุก concept ถูกพิสูจน์สมบูรณ์ / software production-ready / ผู้เรียนเข้าใจแล้ว.

Assessment ด้านความเข้าใจต้องใช้ exercises, evidence submission, mastery rubric และ capstone defense แยกจาก CI.

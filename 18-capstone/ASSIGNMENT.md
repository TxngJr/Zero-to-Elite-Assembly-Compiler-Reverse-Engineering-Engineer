# Final Capstone Assignment — งานที่ผู้เรียนต้องทำเอง

Automated `make test` ของ Chapter 18 เป็น **integration baseline** เท่านั้น. การจบหลักสูตรต้องส่งงานที่แก้/สร้างเองต่อไปนี้.

## Deliverable A — Compiler change (25 pts)

เลือกหนึ่งงาน:

1. เพิ่ม optimization pass ที่ปลอดภัยหนึ่งตัว เช่น algebraic identity ที่มี test ครอบคลุม signed-i64 semantics, หรือ
2. เพิ่ม diagnostic ที่เจาะจงขึ้นพร้อม negative tests, หรือ
3. เพิ่ม IR verifier ที่ตรวจ undefined value / duplicate block / bad branch target.

ต้องส่ง:
- design note
- code patch
- unit tests
- optimized vs unoptimized equivalence evidence
- limitation อย่างน้อย 1 ข้อ

ห้ามนับการเปลี่ยน formatting/comments เป็น implementation.

## Deliverable B — EliteOS64 change (25 pts)

ทำ kernel change ที่สังเกตได้ใน QEMU เช่น:
- เพิ่ม `uptime` command จาก PIT ticks,
- เพิ่ม read-only command สำหรับ boot/memory metadata,
- เพิ่ม diagnostic command ที่ไม่ทำลาย host.

ต้อง:
- build kernel
- ผ่าน static test
- ผ่าน `make -C 14-my-os qemu-test`
- แสดง serial evidence
- อธิบาย kernel/user-space difference

ห้ามอ้าง Chapter 15 simulator ว่า integrate เข้า kernel ถ้ายังไม่ได้ทำจริง.

## Deliverable C — Blind authorized RE (20 pts)

ใช้ binary ที่:
- คุณไม่ได้เปิด source ก่อน,
- เป็น course-owned / generated for training / explicitly authorized.

ส่ง report:
- SHA-256
- ELF triage
- function/basic-block evidence
- reconstructed pseudocode
- dynamic observationอย่างน้อย 1 จุด
- Facts / Inferences / Unknowns แยกชัด
- เปิด sourceภายหลังแล้วบันทึก assumptions ที่ผิด

## Deliverable D — Defensive bug-fix case (20 pts)

ใช้ course-owned code:
1. สร้างหรือเลือก defect ที่ local และปลอดภัย
2. reproduce ด้วย sanitizer/compiler diagnostic/test
3. หา root cause
4. patch
5. regression test
6. fuzz/smoke หลัง fix
7. เขียน impact โดยไม่เกิน evidence

ไม่ต้องและไม่ควรสร้าง exploit.

## Deliverable E — Engineering defense (10 pts)

ตอบโดยไม่เปิด notes อย่างน้อย 10 คำถามจาก `MASTERY_TEST.md`, ต้องมี:
- compiler 2
- ABI/ELF 2
- OS 2
- RE 2
- defensive security 2

## Required submission tree

```text
capstone-submission/
├── README.md
├── compiler/
│   ├── design.md
│   ├── patch.diff
│   └── tests.txt
├── os/
│   ├── design.md
│   ├── patch.diff
│   └── qemu-serial.txt
├── re/
│   └── report.md
├── security/
│   └── report.md
├── evidence/
│   ├── commands.txt
│   ├── tool-versions.txt
│   └── hashes.txt
└── final-report.md
```

## Fail conditions

ถึงคะแนนรวมสูงก็ไม่ผ่านถ้า:
- ไม่มี code modification ของตัวเอง
- ไม่มี QEMU runtime evidence สำหรับ OS deliverable
- RE/security target ไม่มี authorization
- report อ้าง production-ready / secure โดยไม่มีหลักฐาน
- คัด solution โดยไม่อธิบาย design/debugging

## Capstone meaning

เป้าหมายไม่ใช่ “รัน repo ได้” แต่คือพิสูจน์ว่าคุณสามารถ **เปลี่ยนระบบ, ทำนายผล, ตรวจ machine-level evidence, debug failure และอธิบายข้อจำกัด** ได้.

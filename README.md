# Zero to Elite Assembly, Compiler & Reverse Engineering Engineer

หลักสูตร Systems Programming แบบลงมือทำบน Fedora/x86-64 ตั้งแต่พื้นฐาน Linux และการแทนข้อมูล ไปจนถึง C ในมุมมองของเครื่อง ก่อนต่อยอดสู่ Assembly, Compiler, OS และ Reverse Engineering ในบทถัดไป

> เป้าหมายคือสร้างพื้นฐานที่ลึกพอให้คุณออกแบบ ตรวจสอบ ดีบัก และเรียนหัวข้อ systems ขั้นสูงต่อด้วยตนเอง—not เพื่ออ้างว่าจบ repo เดียวแล้วรู้ทุกอย่าง

## วิธีเรียนหลัก

ทุกบทใช้วงจร:

```text
Predict → Build → Run → Observe → Inspect → Debug → Modify → Explain
```

ก่อนรันตัวอย่าง ให้เขียนสิ่งที่คาดว่าจะเกิดขึ้น จากนั้นตรวจผลจริงด้วย compiler/debugger/เครื่องมือระบบ แล้วอธิบายด้วยภาษาของตัวเองว่าเหตุใดจึงเกิดผลนั้น

## Mental model ที่เราจะสร้าง

```text
Source Code
    ↓
Compiler
    ↓
Assembly
    ↓
Machine Code
    ↓
Executable
    ↓
Linux Loader
    ↓
Process
    ↓
CPU Execution
```

ในช่วง Reverse Engineering เราจะฝึกมองย้อนกลับ:

```text
Machine Code
    ↓
Disassembly
    ↓
Control Flow
    ↓
Functions
    ↓
Data Structures
    ↓
Approximate Program Logic
```

## บทที่พร้อมเรียนตอนนี้

- [00 — Linux Systems Laboratory](00-linux-lab/README.md)
- [01 — Computer Foundations](01-computer-foundations/README.md)
- [02 — C Machine Model](02-c-machine-model/README.md)

บท 03–18 มี roadmap ใน [COURSE_MAP.md](COURSE_MAP.md) แต่ยังไม่สร้าง directory จนกว่าจะถึงรอบถัดไป

## แพลตฟอร์ม

หลักสูตรอ้างอิง Fedora Linux บน x86-64/AMD64 เป็นหลัก ใช้ GCC/Clang, GNU binutils, GDB และเครื่องมือ command line มาตรฐาน

ตรวจเครื่อง:

```bash
./scripts/check-environment.sh
```

ติดตั้งเครื่องมือพื้นฐานบน Fedora:

```bash
./scripts/install-fedora-tools.sh
```

ตรวจ Chapter 00–02:

```bash
./scripts/verify-chapters.sh
```

## โครงสร้าง

```text
.
├── README.md
├── COURSE_MAP.md
├── STUDY_GUIDE.md
├── GLOSSARY.md
├── TROUBLESHOOTING.md
├── scripts/
├── 00-linux-lab/
├── 01-computer-foundations/
└── 02-c-machine-model/
```

แต่ละ chapter แยก Objectives, Theory, Labs, Exercises, Challenges, Mastery Test, Answers, Common Mistakes, examples/projects และ tests เพื่อให้เรียนแบบเป็นขั้นตอน

## Prerequisites

ต้องใช้เพียงพื้นฐานการใช้งานคอมพิวเตอร์และความตั้งใจทำ lab เอง ไม่สมมติว่าผู้เรียนรู้ Assembly, Compiler หรือ OS มาก่อน ความรู้ programming เดิมมีประโยชน์แต่ไม่จำเป็น

## กฎการทำแบบฝึก

1. อ่านโจทย์โดยยังไม่ดู `ANSWERS.md`
2. เขียน prediction
3. ทดลองจริง
4. เก็บ output ที่สำคัญ
5. อธิบายความต่างระหว่าง prediction กับผลจริง
6. แก้ exercise/challenge
7. ทำ mastery test เมื่อจบบท

อ่านรายละเอียดใน [STUDY_GUIDE.md](STUDY_GUIDE.md)

## Safety / Reverse Engineering Scope

บทด้าน reverse engineering และ vulnerability research ในอนาคตจะจำกัดอยู่กับโปรแกรมที่สร้างเพื่อหลักสูตร, open-source software, CTF/training binaries, หรือซอฟต์แวร์ที่ผู้เรียนมีสิทธิ์วิเคราะห์ เน้น debugging, understanding, root-cause analysis และ defensive research ไม่สร้างเนื้อหาสำหรับ credential theft, persistence, destructive payloads หรือ unauthorized access

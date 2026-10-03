# Zero to Elite Assembly, Compiler & Reverse Engineering Engineer

หลักสูตร Systems Programming แบบลงมือทำบน Fedora/x86-64 ตั้งแต่ Linux, การแทนข้อมูล, C machine model ไปจนถึง Assembly, ABI/syscalls และ Computer Architecture ก่อนต่อยอดสู่ ELF, Compiler, OS และ Reverse Engineering

> เป้าหมายคือสร้างพื้นฐานที่ลึกพอให้คุณออกแบบ ตรวจสอบ ดีบัก และเรียนหัวข้อ systems ขั้นสูงต่อด้วยตนเอง—not เพื่ออ้างว่าจบ repo เดียวแล้วรู้ทุกอย่าง

## วิธีเรียนหลัก

```text
Predict → Build → Run → Observe → Inspect → Debug → Modify → Explain
```

ก่อนรันตัวอย่าง ให้เขียนสิ่งที่คาดว่าจะเกิดขึ้น จากนั้นตรวจผลจริงด้วย compiler/debugger/disassembler/system tools แล้วอธิบายด้วยภาษาของตัวเอง

## Mental model ที่เรากำลังสร้าง

```text
Source Code
    ↓
Compiler
    ↓
Assembly
    ↓
Machine Code
    ↓
ABI / Linkage
    ↓
Executable
    ↓
Linux Loader / Syscalls
    ↓
Process
    ↓
ISA Execution
    ↓
Microarchitecture / Memory Hierarchy
```

ในช่วง Reverse Engineering เราจะฝึกมองย้อนกลับ:

```text
Machine Code → Disassembly → Control Flow → Functions → Data Structures → Approximate Program Logic
```

## บทที่พร้อมเรียนตอนนี้

- [00 — Linux Systems Laboratory](00-linux-lab/README.md)
- [01 — Computer Foundations](01-computer-foundations/README.md)
- [02 — C Machine Model](02-c-machine-model/README.md)
- [03 — x86-64 Assembly](03-x86-64-assembly/README.md)
- [04 — System V AMD64 ABI & Linux Syscalls](04-abi-syscalls/README.md)
- [05 — Computer Architecture](05-computer-architecture/README.md)

บท 06–18 มี roadmap ใน [COURSE_MAP.md](COURSE_MAP.md) แต่ยังไม่สร้าง chapter directory จนกว่าจะถึงรอบถัดไป

## แพลตฟอร์ม

หลักสูตรอ้างอิง Fedora Linux บน x86-64/AMD64 เป็นหลัก ใช้ GCC/Clang, GNU binutils, GDB, strace และเครื่องมือ command line มาตรฐาน. Chapter 05 ใช้ `perf` เป็น optional measurement toolเมื่อระบบอนุญาต

```bash
./scripts/install-fedora-tools.sh
./scripts/check-environment.sh
./scripts/verify-chapters.sh
```

## โครงสร้างปัจจุบัน

```text
.
├── 00-linux-lab/
├── 01-computer-foundations/
├── 02-c-machine-model/
├── 03-x86-64-assembly/
├── 04-abi-syscalls/
├── 05-computer-architecture/
├── scripts/
├── README.md
├── COURSE_MAP.md
├── STUDY_GUIDE.md
├── GLOSSARY.md
└── TROUBLESHOOTING.md
```

แต่ละ chapter มี Objectives, Theory, Labs, Exercises, Challenges, Mastery Test, Answers, Common Mistakes, examples/projects และ tests ตามความเหมาะสม

## กฎการทำแบบฝึก

1. อ่านโดยยังไม่เปิดเฉลย
2. เขียน prediction
3. build/run
4. เก็บ evidence
5. inspectระดับ source/assembly/register/memory/syscallตามบท
6. อธิบายความต่างระหว่าง prediction กับ observation
7. แก้ exercise/challenge
8. ผ่าน mastery gateก่อนขยับบท

อ่าน [STUDY_GUIDE.md](STUDY_GUIDE.md) เพิ่มเติม

## Safety / Reverse Engineering Scope

งาน reverse engineering/vulnerability researchในอนาคตจำกัดที่ course binaries, open-source software, CTF/training targets หรือซอฟต์แวร์ที่มีสิทธิ์วิเคราะห์ เน้น understanding/debugging/root-cause/defensive research ไม่สร้าง workflowสำหรับ credential theft, persistence, destructive payloads หรือ unauthorized access

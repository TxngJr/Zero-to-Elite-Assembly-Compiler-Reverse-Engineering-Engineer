# Zero to Elite Assembly, Compiler & Reverse Engineering Engineer

หลักสูตร systems engineering แบบลงมือทำบน Linux/x86-64 ตั้งแต่ computer foundations → C/Assembly/ABI → ELF/debugging → compiler → educational kernel → authorized reverse engineering → defensive security.

> ชื่อ repository สื่อถึงเส้นทางระยะยาว. Repository นี้เป็น **educational implementation**, ไม่ใช่คำกล่าวว่า compiler/kernel/security tooling production-ready หรือว่าผู้เรียน “elite” เพียงเพราะ tests ผ่าน.

## Learning loop

```text
Predict → Build → Run → Observe → Inspect → Debug → Modify → Explain
```

## Quality rules

อ่านก่อนเริ่ม:
- [Study Guide](STUDY_GUIDE.md)
- [Assessment Policy](ASSESSMENT_POLICY.md)
- [Course Authoring Standard](COURSE_AUTHORING_STANDARD.md)
- [EliteLang Language Specification](LANGUAGE_SPEC.md)
- [Continuous Integration](CI.md)

ทุก Chapter 00–18 มี:
- `LEARNER_GUIDE.md`
- `WORKED_EXAMPLES.md`
- `EXERCISES.md` พร้อม evidence contract
- `MASTERY_TEST.md`
- `RUBRIC.md` 100 คะแนน

## Roadmap

```text
00 Linux Lab
→ 01 Computer Foundations
→ 02 C Machine Model
→ 03 x86-64 Assembly
→ 04 ABI & Syscalls
→ 05 Computer Architecture
→ 06 ELF
→ 07 Linker & Loader
→ 08 Debugging
→ 09 Compiler Frontend
→ 10 IR + data-flow + SSA construction
→ 11 x86-64 Backend + linear-scan allocation lab
→ 12 EliteC integration
→ 13 OS Foundations
→ 14 EliteOS64 kernel
→ 15 Advanced OS Models & Integration Design
→ 16 Authorized Reverse Engineering
→ 17 Defensive Security Lab
→ 18 Final Capstone
```

## Compiler status

EliteC supports:
- functions/recursion
- signed 64-bit `int` + `bool`
- locals/assignment
- arithmetic/comparisons
- short-circuit logic
- if/else/while
- >6 integer arguments

Semantic contractอยู่ใน [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md).

Chapter 10 now includes educational SSA construction. Chapter 11 includes a tested linear-scan allocator lab, while the **baseline generated code still intentionally uses spill-everything stack slots**.

## OS status

EliteOS64 implements:
- Multiboot2 handoff
- protected→long mode
- early paging/GDT
- serial/VGA
- IDT + common fault diagnostics
- PIC/PIT/keyboard
- memory map / physical-frame allocator
- kernel heap
- interactive serial/PS2 shell

Static check:

```bash
make -C 14-my-os clean test
```

Separate runtime proof:

```bash
make -C 14-my-os qemu-test
```

The QEMU gate waits for real PIT IRQ ticks before declaring the shell ready.

## RE / defensive security scope

Only course-owned or explicitly authorized targets. The focus is debugging, compatibility, root-cause analysis, patching, sanitizers, fuzzing and regression testing.

## Automated repository checks

```bash
./scripts/check-environment.sh
./scripts/verify-chapters.sh
```

Expected final wording:

```text
[OK] Automated repository checks for Chapters 00–18 passed.
```

That does **not** certify learner mastery, security, production readiness, or universal hardware compatibility.

## Final capstone

```bash
make -C 18-capstone clean test
```

is only the integration baseline. Course completion additionally requires learner-created work in [18-capstone/ASSIGNMENT.md](18-capstone/ASSIGNMENT.md).

# Labs

1. **Break/main:** `debug_target.c`; break main/compute_total, info args/locals.
2. **Memory:** inspect struct/arrayด้วย `x/`.
3. **Watchpoint:** watch state totalหรือ countใน lab copy; หา instructionที่เปลี่ยน.
4. **Conditional breakpoint:** stopเฉพาะ iterationหนึ่ง.
5. **Assembly stepping:** `disassemble /r`, si/ni, track registers.
6. **Optimized build:** O0 vs O2; compare locals/backtrace/inlining.
7. **Signal:** `crash_target --crash` ใต้ GDB; inspect SIGSEGV state.
8. **Core dump:** ถ้าระบบอนุญาต ใช้ core/coredumpctl; ถ้าปิดให้บันทึก limitation.
9. **Assertion:** trigger course assertion; distinguish SIGABRT/invariant.
10. **ASan:** build Debug Lab injected bug; อ่าน first invalid access.
11. **Stack corruption concept:** ใช้ sanitizer evidenceก่อนตีความ later crash.
12. **GDB batch:** run `tests/inspect.gdb`; ทำ debugging reproducible.
13. **Shared library:** Chapter 07 shared-demo; breakpoint calc_add, info sharedlibrary.
14. **starti:** follow startupถึง mainแบบ limited steps.
15. **Regression:** เพิ่ม caseที่จับ off-by-one bug.

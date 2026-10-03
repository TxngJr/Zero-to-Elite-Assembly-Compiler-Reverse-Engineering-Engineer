# Objectives

เมื่อจบบทนี้ควรสามารถ:
- สร้าง reproducible bug reportจาก symptom
- ใช้ breakpoints, conditional breakpoints, watchpoints และ catchpointsระดับพื้นฐาน
- อ่าน call stack/backtrace, frame, args, locals
- inspect registers/memory/instructions
- ดีบัก source ↔ assembly
- เข้าใจ debug symbols/DWARF และผลของ stripping
- ดีบัก optimized codeโดยไม่เชื่อ source-variable viewมากเกินไป
- วิเคราะห์ SIGSEGV/SIGABRT/SIGFPEระดับพื้นฐาน
- สร้าง/เปิด core dumpเมื่อระบบอนุญาต
- ใช้ ASan/UBSanร่วมกับ debugger
- แยก root causeจาก crash site
- ใช้ assertions/loggingอย่างมีวินัย
- เพิ่ม regression testหลัง fix
- ใช้ GDB batch scriptเพื่อทำ debugging reproducible

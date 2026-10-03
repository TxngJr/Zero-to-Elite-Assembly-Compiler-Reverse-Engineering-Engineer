# Objectives

เมื่อจบบทนี้ควรสามารถ:

- อธิบาย compiler driverกับ compiler phasesที่อยู่ข้างใน
- ใช้ CLI เดียวเพื่อ check/emit AST/IR/assembly/ELF
- เชื่อม frontend diagnosticsกับ pipeline failure
- เปิด/ปิด optimizationอย่างมี regression tests
- แยก compiler exit statusจาก compiled-program exit status
- เรียก external assembler/linkerผ่าน compiler driverอย่างปลอดภัย
- inspect generated assemblyและ ELF
- ทดสอบ recursion, loops, short-circuit, >6 arguments
- สร้าง deterministic end-to-end compiler test suite
- อธิบายสิ่งที่ยังขาดจาก production compiler เช่น full SSA, register allocation, object emission, debug info, modules, richer types
- วาง architectureสำหรับเพิ่ม language featuresโดยไม่ทำให้ frontend/IR/backendผูกกันแน่นเกินไป

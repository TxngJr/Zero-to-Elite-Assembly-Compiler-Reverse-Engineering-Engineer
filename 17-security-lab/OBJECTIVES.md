# Objectives

เมื่อจบบทนี้ควรสามารถ:

- แยก symptom, crash site และ root cause
- ใช้ ASan/UBSanกับ course-owned code
- อธิบาย out-of-bounds, use-after-free, double-free, integer overflow, format-string and race bug classesเชิง defensive
- เขียน input validationก่อน memory operation
- ตรวจ size arithmetic overflowก่อน allocation/copy
- minimize crashing input
- สร้าง deterministic reproducer
- เขียน regression testที่ failก่อน patch/passหลัง patch
- ใช้ fuzz harnessกับ parser APIที่แยกจาก I/O
- triage sanitizer outputหา error classและ first project frame
- compare vulnerable/fixed sourceหรือ binaryเพื่อทำ patch analysis
- ระบุ impactอย่างระมัดระวังโดยไม่สร้าง exploit
- อธิบาย hardening defense-in-depthเช่น ASLR, NX, RELRO, stack protectorโดยไม่ถือว่าแทน bug fix
- เขียน defensive security reportที่มี scope/evidence/fix/tests

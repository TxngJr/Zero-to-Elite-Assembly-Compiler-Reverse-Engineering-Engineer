# Challenges

- **11-A Linear Scan:** สร้าง live intervalsจาก IRและ allocate caller-saved GPRs พร้อม spills.
- **11-B Smarter Comparisons:** fuse compare+branchเมื่อ bool tempใช้เฉพาะ terminator.
- **11-C Callee-Saved Allocation:** ใช้ RBX/R12–R15พร้อม save/restoreถูก ABI.
- **11-D Differential Tester:** เขียน IR interpreterแล้วสุ่ม deterministic expressionsเพื่อเทียบ executable result.
- **11-E Direct Object Preview:** ออกแบบ required sections/symbols/relocationsหากจะ emit ELF relocatable objectเอง.

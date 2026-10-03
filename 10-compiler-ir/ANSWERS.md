# Answers and Hints

- Basic blockจบเมื่อเจอ jump/cjump/return
- livenessเป็น backward may-analysis: IN=USE∪(OUT-DEF)
- dominatorต้องอยู่บน **ทุก** pathจาก entry
- phiเลือกค่าตาม predecessor edge ไม่ใช่ function call
- course `--ssa` เป็น phi-candidate hint ไม่ใช่ full SSA
- optimizationที่มี calls/divisionต้องระวัง side effects/traps

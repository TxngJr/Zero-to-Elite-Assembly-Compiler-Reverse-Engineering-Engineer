# Answers and Hints

- Basic blockจบเมื่อเจอ jump/cjump/return
- livenessเป็น backward may-analysis: IN=USE∪(OUT-DEF)
- dominatorต้องอยู่บน **ทุก** pathจาก entry
- phiเลือกค่าตาม predecessor edge ไม่ใช่ function call
- course `--ssa` เป็น phi-candidate hint ไม่ใช่ full SSA
- optimizationที่มี calls/divisionต้องระวัง side effects/traps
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

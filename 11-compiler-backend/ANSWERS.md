# Answers and Hints

- stack-slot baselineคือ spill-everything: correctง่ายแต่ memory trafficสูง
- after `push rbp`, subtract frameที่เป็น multiple of 16ทำให้ RSPพร้อมสำหรับ callsใน prologue modelนี้
- stack args push reverse; paddingต้องไม่แทรกระหว่าง return addressกับ arg7
- signed division: `cqo; idiv divisor`
- graph coloringใช้ interference; linear scanใช้ intervals
- short-circuitเกิดตั้งแต่ IR CFG จึงไม่ execute RHSเมื่อ pathไม่ถึง
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

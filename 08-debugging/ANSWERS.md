# Answers and Hints

- Breakpointหยุดที่ control-flow location; watchpointหยุดเมื่อ watched memoryถูก access/changeตามชนิด
- `-g` เพิ่ม debug metadata; ใช้ร่วมกับ `-O2`ได้
- crash siteไม่จำเป็นต้องเป็นจุดสร้าง bad state
- coreต้อง match executable/debug symbols
- ASan first invalid accessมักมีประโยชน์กว่า later allocator/crash symptom
- regression testควร failกับ bugเดิมและ passหลัง fixโดยยึด contract
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

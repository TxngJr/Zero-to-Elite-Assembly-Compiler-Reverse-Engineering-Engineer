# Answers and Hints

- Breakpointหยุดที่ control-flow location; watchpointหยุดเมื่อ watched memoryถูก access/changeตามชนิด
- `-g` เพิ่ม debug metadata; ใช้ร่วมกับ `-O2`ได้
- crash siteไม่จำเป็นต้องเป็นจุดสร้าง bad state
- coreต้อง match executable/debug symbols
- ASan first invalid accessมักมีประโยชน์กว่า later allocator/crash symptom
- regression testควร failกับ bugเดิมและ passหลัง fixโดยยึด contract

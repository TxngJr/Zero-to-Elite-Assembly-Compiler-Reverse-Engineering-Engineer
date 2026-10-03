# Common Mistakes

- Hex เป็น “ค่าอีกชนิด” — จริง ๆ เป็น notation
- MSB=1 แปลว่าติดลบเสมอ — ต้องรู้ signed interpretation
- `0xFF=-1` เสมอ — unsigned 8-bit คือ 255
- Signed C overflow wrap เสมอ — ผิด; เป็น UB
- Shift = multiply/divide เสมอ — ต้องดู type/width/rules
- Address = physical RAM — user process ปกติเห็น virtual address
- Little endian กลับ bits — เป็น byte order
- Unaligned access ใช้ไม่ได้ทุก CPU — architecture-specific
- Fetch→Decode→Execute เป็น timing จริงทั้งหมด — เป็น simplified teaching model

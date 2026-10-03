# Answers and Hints

- 64-byte block → offset 6 bits; 256 sets → index 8 bits; ที่เหลือ tag
- TLB missเพียงหมายถึง translationไม่อยู่ TLB; page-table walkอาจสำเร็จโดยไม่มี page fault
- register renamingลบ name dependencies WAR/WAW แต่ไม่ลบ true RAW dependency
- coherenceเน้น locationเดียว; consistencyกำหนด ordering modelกว้างกว่า
- Amdahl P=0.8,S=4 → `1 / (0.2 + 0.8/4) = 2.5×`
- branch predictor projectเป็น educational model ไม่ใช่คำอธิบาย predictorจริงของ CPUรุ่นใดรุ่นหนึ่ง

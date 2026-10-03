# Answers and Hints

- 173 = `10101101₂` = `0xAD`
- `0xA7` = `10100111₂` = 167
- `11111011₂` = 251 unsigned = -5 signed 8-bit
- 16-bit unsigned 0..65535; signed -32768..32767
- little-endian `0xDEADBEEF` → `EF BE AD DE`

Methods: binary→hex จับกลุ่ม 4 bits; signed two's complement ใช้ `unsigned-2^n` เมื่อ high bit=1; field mask สร้าง width bits แล้ว shift; little-endian reconstruction ให้ byte ต่ำสุดคูณ `256^0`.

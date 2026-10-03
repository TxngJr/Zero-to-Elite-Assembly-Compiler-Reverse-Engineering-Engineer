# Challenges

- **05-A Tiny CPU ISA extension:** เพิ่ม AND/XOR/conditional branch พร้อม assembler-like encoder helperและ tests.
- **05-B 2-way cache:** ขยาย cache simulatorเป็น 2-way set associative + LRU; compare conflict traceกับ direct-mapped.
- **05-C Cache trace generator:** C programสร้าง row/column access tracesแล้ว feed cache simulatorเพื่อเทียบ misses.
- **05-D Predictor tournament:** implement always-taken, 1-bit, 2-bit predictorsและ compare accuracyบนหลาย synthetic patternsโดยไม่อ้างผลแทน real CPU predictor.
- **05-E Amdahl report:** เลือก workloadจำลองที่แบ่ง serial/parallel fractionsและคำนวณ theoretical ceilingหลาย S values.

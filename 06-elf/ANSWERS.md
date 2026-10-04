# Answers and Hints

- Magic = `7f 45 4c 46`
- `e_entry` เป็น virtual address
- `PT_LOAD`: map file rangeไป memory rangeพร้อม permissions
- `.bss` มัก `SHT_NOBITS`; runtime zerosไม่ต้องอยู่ใน fileครบ
- `.symtab` stripได้; `.dynsym` เก็บ dynamic-link subset
- relocatable objectมี undefined symbolsได้
- PIEมัก `ET_DYN`; ET_DYNไม่เท่ากับ libraryเสมอ
- Parserต้องตรวจ overflowก่อน `offset + count*size`
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

# Answers and Hints

- Lexerตอบ “tokenอะไร”; parserตอบ “structureอะไร”; checkerตอบ “meaning/typeนี้อนุญาตไหม”
- precedenceต้องทำให้ `* / %` bindแน่นกว่า `+ -`
- function signaturesควร collectก่อน check bodiesเพื่อรองรับ forward calls/recursion
- syntax-validไม่ได้หมายถึง semantic-valid
- scope stackหรือ persistent environmentsช่วย nested blocks; course versionห้าม shadowingเพื่อให้ชื่อ IRเรียบง่าย
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

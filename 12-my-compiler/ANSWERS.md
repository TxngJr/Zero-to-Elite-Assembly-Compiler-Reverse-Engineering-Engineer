# Answers and Hints

- Driver orchestrationไม่ใช่ phase semanticsเอง
- Behavioral testsสำคัญกว่า assembly-string snapshots
- Full compilerยัง correctได้แม้ backend spillทุก value
- `--opt` ต้องเปลี่ยน implementationโดยไม่เปลี่ยน supported observable behavior
- Self-hostingเป็น milestoneด้าน bootstrapping ไม่ใช่นิยามขั้นต่ำของ compiler
- Bare-metal targetไม่มี process startup/libc assumptionsแบบ Linux user-space
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

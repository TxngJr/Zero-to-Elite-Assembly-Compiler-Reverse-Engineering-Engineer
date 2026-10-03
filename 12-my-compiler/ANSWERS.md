# Answers and Hints

- Driver orchestrationไม่ใช่ phase semanticsเอง
- Behavioral testsสำคัญกว่า assembly-string snapshots
- Full compilerยัง correctได้แม้ backend spillทุก value
- `--opt` ต้องเปลี่ยน implementationโดยไม่เปลี่ยน supported observable behavior
- Self-hostingเป็น milestoneด้าน bootstrapping ไม่ใช่นิยามขั้นต่ำของ compiler
- Bare-metal targetไม่มี process startup/libc assumptionsแบบ Linux user-space

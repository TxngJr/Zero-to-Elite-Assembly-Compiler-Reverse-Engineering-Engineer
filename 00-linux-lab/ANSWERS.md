# Answers and Hints

ใช้หลังจากลองเองแล้ว

- Ex.5: `rwx=7`, `r-x=5`, `---=0`
- Ex.8: creation mode ถูก mask ด้วย complement ของ umask; application/object type ก็มีผล
- Ex.12: redirection ทำซ้าย→ขวา; `2>&1` duplicate destination ณ เวลานั้น
- Ex.18: source → preprocessor → compiler → assembler → linker
- Ex.22: optimizer สามารถ transform/remove source-level objects ตาม language semantics

Challenge 00-B: redirect streams, เก็บ exit code ก่อน command อื่นจะทับ `$?`, แล้ว `exit "$status"`.

Reference: `.i` = preprocessed source, `.s` = assembly text, `.o` = relocatable object, final executable = linked image.
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

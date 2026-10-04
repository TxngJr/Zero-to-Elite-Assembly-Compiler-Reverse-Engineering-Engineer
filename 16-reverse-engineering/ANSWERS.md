# Answers and Hints

- O2 may inline/remove/reorder source constructs; compare semantics, not line count.
- PIE runtime address = load base + image-relative address in common model.
- Struct recovery from offsets gives layout evidence but source field names/types may remain uncertain.
- A stripped binary can still contain dynamic symbols/unwind/dynamic metadata.
- Dynamic evidence proves what happened on observed executions, not all possible paths.
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

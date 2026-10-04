# Answers and Hints

- Validate `claimed <= input_remaining` **and** `claimed <= destination_capacity` before copy.
- Check arithmetic before performing overflow-prone operation.
- Sanitizers find many bugs but clean runไม่ prove absence.
- Fuzzing works best with deterministic harness + structured seeds + regression of discovered cases.
- Hardening reduces consequences/attack surfaceบางส่วน; correct patch removes root cause.
- Describe impact only under conditions demonstrated by evidence.
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

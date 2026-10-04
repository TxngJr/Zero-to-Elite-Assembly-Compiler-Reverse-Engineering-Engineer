# Answers and Hints

- COW forkแชร์ framesพร้อม read-only+COW metadata; write faultค่อย copyเมื่อจำเป็น.
- Context switchต้องคิดทั้ง CPU registers, stackและ address space—not RIPอย่างเดียว.
- TSS RSP0ให้ privileged stackเมื่อ transitionจาก ring3.
- Pipe ring bufferแยก storage semanticsจาก scheduler blocking policy.
- VFS path lookupกับ file-open stateเป็นคนละ layer.
- SMP correctnessต้องเพิ่ม synchronization/memory ordering; single-core correctnessไม่พอ.
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

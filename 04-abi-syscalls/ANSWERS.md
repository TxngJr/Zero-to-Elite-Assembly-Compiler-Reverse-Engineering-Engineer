# Answers and Hints

- SysV integer args: RDI,RSI,RDX,RCX,R8,R9; 7+บน stack
- callee-saved: RBX,RBP,R12–R15; caller-saved: RAX,RCX,RDX,RSI,RDI,R8–R11
- ก่อน `call` RSP 16-byte aligned; entryหลัง return-address pushมัก `rsp % 16 == 8`
- raw Linux syscall: RAX number; RDI,RSI,RDX,R10,R8,R9; RCX/R11 clobbered
- raw failure = negative errno; libcมักแปลงเป็น -1 + `errno`
- `_start`: `[rsp]=argc`, `[rsp+8]=argv[0]`, `[rsp+16]=argv[1]` ก่อนปรับ stack
- partial write: advance pointerและลด remainingจน 0
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

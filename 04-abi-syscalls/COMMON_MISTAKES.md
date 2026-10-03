# Common Mistakes

- คิดว่า ISAกำหนด RDI/RSI argsแทน ABI
- ใช้ RCXเป็น syscall arg4แทน R10
- ลืม RCX/R11 clobber
- clobber RBX/R12–R15โดยไม่ restore
- stack alignmentผิดก่อน nested call
- assumeทุก functionมี RBP frame
- ใช้ red zoneใน contextที่ไม่รับประกัน
- raw syscall failแล้วคาด errnoถูก set
- writeครั้งเดียวแล้วสมมติครบ
- hard-code syscall numbersแล้วเรียก portable
- `_start` จบด้วย `ret`
- อ่าน argv offsetsหลังเปลี่ยน RSPโดยไม่คำนวณใหม่

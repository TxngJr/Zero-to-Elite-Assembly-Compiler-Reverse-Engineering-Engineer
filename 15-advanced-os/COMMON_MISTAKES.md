# Common Mistakes

- process = threadเสมอ
- context switchแค่เปลี่ยน RIP
- user pointerเชื่อถือได้เพราะมาจาก processของเรา
- forkต้อง copy physical memoryทันทีทั้งหมด
- COW pageยัง writableทั้งสอง process
- round robinเหมาะที่สุดทุก workload
- blocked taskยังอยู่ runnable queue
- spinlockแล้ว sleepขณะถือ lock
- volatileแทน atomic/lockได้
- VFS inodeกับ open-file offsetเป็น objectเดียวกัน
- CR3 switchไม่มี TLB implications
- SMPเพิ่ม coreแล้ว code single-coreจะ correctเอง

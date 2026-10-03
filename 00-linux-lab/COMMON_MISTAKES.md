# Common Mistakes

- **Terminal = Shell** — terminal ให้ I/O session; shell เป็น command interpreter
- **File name = file object** — directory entry/name กับ underlying object ไม่ใช่แนวคิดเดียวกัน
- **Symlink = hard link** — symlink เก็บ target path; hard link อ้าง object เดียวกัน
- **`755` คือ decimal** — permission notation นี้ตีความเป็น octal digits
- **`kill` แปลว่า force terminate** — command ส่ง signal; default ปกติคือ SIGTERM
- **stdout/stderr รวมกันเสมอ** — เป็นคนละ file descriptor แม้ terminal แสดงปะปน
- **`/proc` เป็นไฟล์บน disk ปกติ** — เป็น virtual/pseudo filesystem interface
- **GCC คือ compiler stage เดียว** — `gcc` command ทำหน้าที่ driver ของหลาย build stages
- **`.o` คือ executable พร้อมรัน** — relocatable object ปกติยังต้อง link
- **สิ่งที่เห็นจากเครื่องหนึ่ง = กฎ Linux ทั้งหมด** — แยก distro convention, ABI และ observation

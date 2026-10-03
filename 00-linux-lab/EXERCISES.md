# Exercises

1. อธิบาย terminal emulator กับ shell คนละหน้าที่อย่างไร
2. `program` กับ `process` ต่างกันอย่างไร
3. จาก `/home/alice/course/00-linux-lab` path `../README.md` resolve ไปที่ใด
4. เปรียบเทียบ `cp a b`, `ln a b`, `ln -s a b`
5. แปลง `rwxr-x---` เป็น octal
6. แปลง `640` เป็น symbolic mode
7. execute bit ของ directory ต่างจาก regular file อย่างไร
8. `umask 022` ไม่ได้แปลว่าไฟล์ใหม่ทุกไฟล์เป็น `022` เพราะอะไร
9. หาก `PATH=/opt/demo/bin:/usr/bin` shell จะค้น `gcc` อย่างไร
10. ทำไมไม่ควรเพิ่ม `.` ไว้หน้า PATH โดยไม่เข้าใจความเสี่ยง
11. file descriptor 0/1/2 คืออะไร
12. อธิบายความต่าง `cmd >a 2>&1` กับ `cmd 2>&1 >a`
13. ใน pipeline ใครเป็น producer/consumer
14. PID กับ PPID บอกอะไร
15. `kill PID` โดย default ไม่เท่ากับ SIGKILL อย่างไร
16. exit status 0 ตาม convention หมายถึงอะไร
17. `/proc` ต่างจาก regular disk directory อย่างไร
18. เรียง stage: assembler, preprocessor, linker, compiler
19. `.c`, `.i`, `.s`, `.o`, executable ต่างกันอย่างไร
20. `file` กับ `readelf -h` ตอบคำถามต่างกันอย่างไร
21. `nm hello.o` ใช้สังเกตอะไรขั้นต้น
22. เหตุใด GDB อาจแสดง source variable เป็น `<optimized out>`
23. Make dependency ช่วย incremental build อย่างไร
24. Git working tree, staging area, commit ต่างกันอย่างไร
25. อธิบาย observation vs platform guarantee พร้อมตัวอย่างหนึ่งกรณี

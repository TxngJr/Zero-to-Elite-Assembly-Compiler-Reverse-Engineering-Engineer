# Mastery Test

## Part A — Concepts
1. วาด Terminal → Shell → Program → Kernel
2. อธิบาย program/process
3. hard link กับ symlink ต่างกันอย่างไร
4. แปลง `rwxr-x---` ↔ octal
5. อธิบาย PATH search
6. อธิบาย fd 0/1/2 และ pipe
7. PID/PPID/exit status/signal คืออะไร
8. `/proc/self` หมายถึงอะไร

## Part B — Predict
9. ทำนาย stdout/stderr จาก `./x >a 2>b`
10. ทำนาย stage outputs ของ `gcc -E`, `-S`, `-c`
11. ทำนาย Make rebuild จาก dependency timestamps

## Part C — Debug
12. script มี Permission denied; ให้ diagnosis อย่างน้อย 3 ขั้นโดยไม่เริ่มจาก sudo
13. GDB ไม่เห็น symbols; อธิบาย build change
14. Makefile ขึ้น missing separator; ตรวจอะไร

## Part D — Build
15. จาก `examples/hello.c` สร้าง `.i`, `.s`, `.o`, executable
16. แสดงหลักฐาน object/executable ต่าง file type
17. breakpoint `add` ใน `debug_me`, แสดง backtrace และ arguments

Pass: concept/prediction/debug ≥85%, `make test` ผ่าน และอธิบาย Lab 00-09/10 ได้

# Challenges

## Challenge 00-A — Evidence-driven system report
สร้าง `system-report.txt` โดยไม่ใช้ sudo ให้มี distro, kernel, architecture, shell PID/PPID, compiler versions, gcc path, logical CPUs และ RAM summary พร้อม command evidence.

## Challenge 00-B — Stream router
เขียน shell script ที่เรียก `examples/streams.c` binary แล้วเก็บ stdout/stderr คนละไฟล์, แสดง stderr บน terminal และคืน exit status เดิม. เก็บ `$?` ทันทีหลัง program.

## Challenge 00-C — Rebuild detector
แก้ Makefile ให้ target rebuild เมื่อ source เปลี่ยน แต่ไม่ rebuild เมื่อไม่มีอะไรเปลี่ยน. ยืนยันด้วย timestamps.

## Challenge 00-D — Process evidence
สร้าง background process ของตัวเอง, บันทึก PID, หา PPID, inspect `/proc/PID/status`, ส่ง SIGTERM และพิสูจน์ว่า process หายไป. ห้ามใช้ PID ที่ไม่ได้สร้างเอง.

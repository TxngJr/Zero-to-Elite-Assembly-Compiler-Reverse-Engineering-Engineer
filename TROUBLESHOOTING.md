# Troubleshooting

## `gcc: command not found`
ตรวจด้วย `command -v gcc`. ถ้าไม่มีและใช้ Fedora ให้รัน `./scripts/install-fedora-tools.sh` หรือ `sudo dnf install gcc`.

## `Permission denied` ตอนรัน script
ตรวจ `ls -l script.sh`. ถ้าไม่มี execute bit ใช้ `chmod +x script.sh`. อีกทางคือ `bash script.sh`.

## `Permission denied` ตอนรันไฟล์ใน filesystem ที่ mount `noexec`
ตรวจ `findmnt -T . -o OPTIONS`. ย้าย lab ไป filesystem ที่อนุญาต execute แทนการเปลี่ยน mount โดยไม่เข้าใจผลกระทบ.

## GDB แสดง `No debugging symbols found`
compile ด้วย `-g`, เช่น `gcc -O0 -g demo.c -o demo`. หากเปิด optimization variables อาจถูกย้าย/รวม/ตัดออกได้.

## `fatal error: ...: No such file or directory`
ดูว่าขาด header จาก development package ใดด้วย `dnf provides '*/header.h'`; อย่าติดตั้ง package สุ่ม ๆ โดยไม่อ่านผลค้นหา.

## `make: *** missing separator`
recipe ของ Makefile ต้องเริ่มด้วย TAB จริงใน Make แบบดั้งเดิม ตรวจด้วย editor ที่แสดง whitespace.

## Sanitizer report ยาวมาก
อ่านจากบรรทัด error type → stack trace แรกที่ชี้ไฟล์ของเรา → address/operation → allocation/free trace ที่เกี่ยวข้อง แก้ root cause ก่อน warning รอง.

## ตัวแปรหายเมื่อดู assembly/GDB
ลอง `-O0 -g` เพื่อ experiment ที่ตรง source มากขึ้น แต่จำไว้ว่า compiler ไม่รับประกันว่าทุก source variable ต้องมี memory slot.

## `readelf`/`objdump` ไม่พบ
ทั้งคู่มาจาก GNU binutils บน Fedora: `sudo dnf install binutils`.

## Build ผ่าน GCC แต่ Clang เตือนต่างกัน
อ่าน diagnostic ทั้งสองตัว Compiler มี wording/analysis ต่างกันได้ ใช้มาตรฐาน C และ tests เป็นหลักแทนการคาดว่า warnings ต้องเหมือนกันทุกบรรทัด

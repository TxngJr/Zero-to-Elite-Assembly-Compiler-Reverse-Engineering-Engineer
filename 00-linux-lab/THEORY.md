# Theory — Linux Systems Laboratory

## 1. Terminal, Shell, Command, Program, Process

**Terminal emulator** คือโปรแกรมที่ให้หน้าต่าง/ช่องทางสำหรับ terminal session ส่วน **shell** เช่น Bash คือ command interpreter ที่อ่านข้อความของเราแล้วตัดสินใจว่าจะใช้ shell builtin หรือหา executable จาก `PATH`.

```text
Keyboard
   ↓
Terminal emulator
   ↓
Shell (bash)
   ↓
Program
   ↓
Linux kernel
```

คำว่า **program** หมายถึงชุดคำสั่ง/ไฟล์โปรแกรม ส่วน **process** คือ execution instance ที่มี PID, address space, file descriptors และ state ของตัวเอง โปรแกรมเดียวเปิดหลายครั้งจึงเกิดหลาย process ได้

ตรวจ shell ปัจจุบัน:

```bash
echo "$SHELL"
ps -p $$ -o pid,ppid,comm,args
```

`$$` คือ PID ของ shell ใน Bash context นี้

## 2. Filesystem mental model

Linux filesystem มี root `/`. `~` โดย shell มัก expand เป็น home directory ของ user, `.` คือ current directory, `..` คือ parent.

- absolute path เริ่มจาก `/`, เช่น `/usr/bin/gcc`
- relative path ตีความจาก current working directory, เช่น `examples/hello.c`

คำสั่งสำคัญ:

```bash
pwd
ls -la
cd path
mkdir demo
touch demo/file
cp demo/file demo/copy
mv demo/copy demo/renamed
file demo/renamed
stat demo/renamed
```

`rm` ลบชื่อ directory entry และไม่มี trash semantics แบบ desktop โดยอัตโนมัติใน command line อย่าฝึกด้วย path นอก lab.

## 3. Directory สำคัญ

- `/usr/bin` — user-facing executables จำนวนมาก
- `/usr/lib`, `/usr/lib64` — libraries/support files ตาม distro/architecture
- `/etc` — system-wide configuration
- `/home` — home directories ของ users ทั่วไป
- `/tmp` — temporary storage; lifecycle ขึ้นกับระบบ
- `/var` — variable data เช่น logs/cache/state
- `/proc` — pseudo-filesystem ที่ kernel expose process/system state
- `/sys` — kernel/device model interface
- `/dev` — device nodes และ pseudo devices

ระบบ Linux สมัยใหม่จำนวนมากใช้ **usr-merge** ทำให้ `/bin` อาจเป็น symlink ไป `/usr/bin`; อย่าสรุปจากชื่อ path อย่างเดียว ใช้ `readlink -f /bin` ตรวจจริง

## 4. Files, inode concept, links

ชื่อไฟล์ใน directory ชี้ไปยัง filesystem object/inode concept ที่เก็บ metadata และอ้างถึง data blocks. `ls -li` แสดง inode number ใน filesystem ที่รองรับแนวคิดนี้

```bash
printf 'alpha\n' > original.txt
cp original.txt copy.txt
ln original.txt hard.txt
ln -s original.txt symbolic.txt
ls -li
readlink symbolic.txt
```

- copy: object/data แยกใหม่
- hard link: directory entry อีกชื่อที่อ้าง object เดียวกัน
- symbolic link: file ชนิดพิเศษที่เก็บ target path

ลบ `original.txt` แล้ว hard link ยังเข้าถึง object เดิมได้ถ้ายังมี link count เหลือ แต่ symlink ที่ชี้ชื่อเดิมอาจกลายเป็น dangling link

## 5. Permissions

Mode เช่น `rwxr-xr-x` แบ่งเป็น owner/group/other:

```text
rwx r-x r-x
421 421 421
 7   5   5  → 755
```

สำหรับ regular file: `r` อ่าน content, `w` เปลี่ยน content, `x` execute. สำหรับ directory semantics ต่างออกไป: `x` เกี่ยวกับ traversal/search, `r` อ่าน directory entries, `w` เปลี่ยน entries เมื่อ permission อื่นเอื้อ

```bash
id
groups
umask
chmod 640 file
chmod u+x script.sh
```

`umask` ไม่ใช่ permission ที่ไฟล์จะได้รับโดยตรง แต่เป็น mask ที่ตัด permission บาง bits จาก requested creation mode

## 6. Environment Variables และ PATH

Environment คือ key/value strings ที่ process ส่งต่อไป child process ได้

```bash
printenv HOME
printf '%s\n' "$PATH"
export DEMO=value
```

เมื่อพิมพ์ command ที่ไม่มี slash shell จะค้นตาม directories ใน `PATH` ตามลำดับ

ทดลองแบบชั่วคราว:

```bash
mkdir -p ./tmp-bin
printf '#!/usr/bin/env bash\necho local-tool\n' > ./tmp-bin/mytool
chmod +x ./tmp-bin/mytool
PATH="$PWD/tmp-bin:$PATH" mytool
```

การ prefix assignment แบบนี้จำกัด environment change ให้ invocation/command context มากกว่าการแก้ `~/.bashrc` ถาวร

## 7. stdin, stdout, stderr และ file descriptors

Convention ของ Unix process:

```text
fd 0 → stdin
fd 1 → stdout
fd 2 → stderr
```

Shell redirection:

```bash
command >out.txt
command >>out.txt
command 2>err.txt
command <input.txt
command >all.txt 2>&1
```

ลำดับ redirection สำคัญ เพราะ shell ทำจากซ้ายไปขวา

## 8. Pipes

Pipe เชื่อม stdout ของ process หนึ่งกับ stdin ของอีก process:

```text
producer stdout → pipe buffer → consumer stdin
```

ตัวอย่าง:

```bash
printf 'pear\napple\npear\n' | sort | uniq -c
```

Pipeline ไม่ได้หมายถึง process แรกเขียนไฟล์ชั่วคราวก่อนเสมอ; kernel จัดการ pipe object และ scheduler interleave processes ได้

## 9. Processes, PID, PPID, status, signals

```bash
sleep 30 &
pid=$!
ps -o pid,ppid,state,comm -p "$pid"
kill "$pid"
wait "$pid"
printf 'exit=%d\n' "$?"
```

`$!` คือ PID ของ background job ล่าสุดใน shell. `kill` โดย default ส่ง signal (`SIGTERM`) ไม่ได้แปลว่า force-kill เสมอ. ใช้ process ที่เราสร้างเองใน lab.

Exit status ตาม convention คือ 0 = success, nonzero = failure/other outcome ตามโปรแกรมกำหนด

## 10. `/proc`

`/proc` ไม่ใช่ directory ของไฟล์ disk ปกติ แต่เป็น kernel interface:

```bash
cat /proc/version
head /proc/meminfo
head /proc/cpuinfo
ls -l /proc/$$/fd
cat /proc/$$/status
```

`/proc/self` resolve ตาม process ที่กำลังอ่านมัน ดังนั้น command ต่าง process อาจเห็น `self` คนละ PID

## 11. Build toolchain overview

สำหรับ C แบบง่าย:

```text
hello.c
  │ gcc -E
  ▼
hello.i        preprocessed C
  │ gcc -S
  ▼
hello.s        assembly text
  │ gcc -c
  ▼
hello.o        relocatable object
  │ linker
  ▼
hello          executable ELF
```

ทดลอง:

```bash
gcc -E examples/hello.c -o build/hello.i
gcc -S -O0 examples/hello.c -o build/hello.s
gcc -c -O0 -g examples/hello.c -o build/hello.o
gcc build/hello.o -o build/hello
```

`gcc` เป็น driver ที่เรียก stage/tool ที่เหมาะสม; อย่าคิดว่า `gcc` คือ stage เดียวเสมอ

Inspection ขั้นต้น:

```bash
file build/hello
readelf -h build/hello
nm build/hello.o
objdump -d build/hello
```

บทนี้เพียงสังเกต structure; ELF และ assembly จะเรียนลึกภายหลัง

## 12. Make

Make สร้าง dependency graph จาก targets/prerequisites และ recipe:

```make
build/hello: examples/hello.c
	mkdir -p build
	gcc -std=c17 -Wall -Wextra -g $< -o $@
```

ถ้า target ใหม่กว่า prerequisite Make อาจไม่ rebuild. นี่คือ incremental build idea. Recipe line ใน Makefile แบบมาตรฐานเริ่มด้วย TAB

## 13. Git basics

```bash
git status
git diff
git add path
git diff --cached
git commit -m 'message'
git log --oneline --decorate -5
git branch
```

Mental model ขั้นต้น: working tree → staging/index → commit history.

## 14. First GDB model

Compile พร้อม debug info:

```bash
gcc -O0 -g examples/debug_me.c -o build/debug_me
gdb ./build/debug_me
```

ภายใน GDB:

```text
break main
run
next
step
print x
info registers
backtrace
disassemble /m main
quit
```

Source variable ไม่จำเป็นต้องคงอยู่เป็น memory slot โดยเฉพาะเมื่อ optimize; ใช้ `-O0` ใน lab แรกเพื่อลดความซับซ้อน แต่ต้องจำว่านี่ไม่ใช่ guarantee ทั่วไป

## 15. หลักฐานสำคัญกว่า intuition

Systems engineering ต้องแยกสามอย่าง:

1. **language rule**
2. **ABI/OS contract**
3. **observation ของ build นี้**

อย่าเอา observation หนึ่งครั้งไปอ้างเป็นกฎสากลโดยไม่มีหลักฐาน

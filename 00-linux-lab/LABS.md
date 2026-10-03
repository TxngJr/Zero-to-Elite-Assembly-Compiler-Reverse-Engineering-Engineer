# Labs

ทุก lab ให้เขียน Prediction ก่อนรัน และตอบ Reflection หลังรัน

## Lab 00-01 — Explore Linux Environment
**Goal:** แยก terminal/shell/process และเก็บ system facts  
**Prediction:** `$$` จะสัมพันธ์กับ `ps -p $$` อย่างไร  
**Run:** `echo "$SHELL"`, `ps -p $$ -o pid,ppid,comm,args`, `uname -a`, `pwd`  
**Observe:** shell executable, PID/PPID, kernel, working directory  
**Explain:** terminal window กับ shell process เป็น object เดียวกันหรือไม่  
**Cleanup:** ไม่มี

## Lab 00-02 — Files, Copy, Hard Link, Symlink
สร้าง `labs/work-links`, ไฟล์ `original`, copy, hard link, symlink; ใช้ `ls -li`, `stat`, `readlink` ก่อนและหลังแก้ content และลบชื่อ `original`. Cleanup เฉพาะ work directory หลังตรวจ `pwd`.

## Lab 00-03 — Permissions
สร้าง script ใน `labs/work-perm`, เริ่ม mode ไม่มี execute, ทำนายผลเมื่อ `./script.sh` และ `bash script.sh`, จากนั้น `chmod u+x`. แปลง `640`, `750`, `755` ด้วยมือก่อนตรวจจริง.

## Lab 00-04 — PATH Experiment
สร้าง executable `mytool` ใน `labs/work-path/bin`; ตรวจ `command -v mytool` ก่อนและหลัง `PATH="$PWD/labs/work-path/bin:$PATH"`. ห้ามแก้ `.bashrc`.

## Lab 00-05 — stdout/stderr
Build `examples/streams.c` แล้วแยก streams ด้วย `>labs/out.txt 2>labs/err.txt`. อธิบาย file descriptors และลำดับ redirection.

## Lab 00-06 — Pipeline Construction
ใช้ `labs/pipeline.txt` แล้วสร้าง pipeline `sort | uniq -c | sort -nr`. อธิบายว่าแต่ละ process อ่าน/เขียนอะไร.

## Lab 00-07 — Process Inspection
รัน `sleep 60 &`, บันทึก `$!`, inspect ด้วย `ps`, ส่ง SIGTERM, `wait`, อ่าน exit status. ใช้เฉพาะ PID ที่สร้างใน lab.

## Lab 00-08 — `/proc`
เปรียบเทียบ `/proc/$$/status`, `/proc/$$/fd`, `/proc/meminfo`, `/proc/cpuinfo`. ระบุ process-specific/system-wide.

## Lab 00-09 — C Build Pipeline

```bash
gcc -E examples/hello.c -o build/hello.i
gcc -S -O0 examples/hello.c -o build/hello.s
gcc -c -O0 -g examples/hello.c -o build/hello.o
gcc build/hello.o -o build/hello
file build/hello.o build/hello
readelf -h build/hello
nm build/hello.o
objdump -d build/hello | head -80
```

ก่อนแต่ละ step ทำนายว่า output เป็น text/binary และ executable หรือไม่.

## Lab 00-10 — First GDB Session
Build `examples/debug_me.c` ด้วย `-O0 -g`; breakpoint ที่ `main` และ `add`; ใช้ `next`, `step`, `print`, `backtrace`, `info registers`. วาด call chain.

## Lab Completion Template

```text
Prediction:
Commands/code:
Observed:
Evidence:
Explanation:
One modification I tried:
Result after modification:
Cleanup performed:
```

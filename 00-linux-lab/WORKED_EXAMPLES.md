# Worked Examples — Linux Systems Laboratory

ใช้วงจร **Predict → Run → Observe → Explain → Modify**. ค่าพวก PID/path/version อาจต่าง; ให้ดู semantic evidence.

## Example 1 — Shell, process และ PID

**Goal:** แยก terminal emulator, shell และ process.

**Prediction:** `$$` ใน Bash ควรตรงกับ PID ที่ `ps -p $$` แสดง.

**Command / action:**

```bash
printf 'shell=%s\n' "$SHELL"
printf 'bash_pid=%s\n' "$$"
ps -p $$ -o pid,ppid,comm,args
```

**Expected key evidence:** PID ที่ Bash expand จาก `$$` ตรงกับแถว `ps`; PPIDคือ process parentและอาจเป็น terminal/session manager.

**What may vary:** PID, PPID, shell path, terminal program.

**Explain:** terminalเป็น I/O endpoint/UI; shellเป็น processหนึ่งที่อ่าน commandและ launch child processes.

**Modification:**

```bash
bash -c 'printf "child shell pid=%s parent=%s\n" "$$" "$PPID"'
```

ทำนาย PID ใหม่ก่อนรัน.

**Failure mode:** อย่าสรุปว่า `$SHELL` เท่ากับ shell processปัจจุบันเสมอ; ตัวแปรนี้มักบอก login/default shell.

**Reflection:** เขียน process treeเล็ก ๆ terminal → shell → command.

---

## Example 2 — stdout/stderr และ redirection order

**Goal:** เห็น fd 1 กับ fd 2 แยกกันจริง.

**Command / action:**

```bash
make -C 00-linux-lab clean all
mkdir -p 00-linux-lab/build/redir

00-linux-lab/build/streams \
  >00-linux-lab/build/redir/out.txt \
  2>00-linux-lab/build/redir/err.txt

printf '%s\n' '--- stdout ---'
cat 00-linux-lab/build/redir/out.txt
printf '%s\n' '--- stderr ---'
cat 00-linux-lab/build/redir/err.txt
```

**Prediction:** stdoutอยู่ `out.txt`, stderrอยู่ `err.txt`.

**Expected key evidence:** เนื้อหา streamสองฝั่งไม่ปนกัน.

**What may vary:** exact message textถ้า example sourceเปลี่ยน.

**Explain:** shellเปิด/duplicate file descriptorsก่อน exec program.

**Modification:** เปรียบเทียบ:

```bash
00-linux-lab/build/streams >a.txt 2>&1
00-linux-lab/build/streams 2>&1 >b.txt
```

อธิบายว่าทำไมลำดับซ้าย→ขวาทำให้ผลต่าง.

**Failure mode:** ถ้ารันคำสั่งอื่นก่อนเก็บ `$?` ค่า exit statusเดิมจะถูกทับ.

**Reflection:** วาด fd tableก่อนและหลัง redirection.

---

## Example 3 — C source → preprocessor → assembly → object → executable

**Goal:** เห็น representationเปลี่ยนทีละ stage.

**Command / action:**

```bash
mkdir -p 00-linux-lab/build/pipeline

gcc -E 00-linux-lab/examples/hello.c \
  -o 00-linux-lab/build/pipeline/hello.i

gcc -S -O0 00-linux-lab/examples/hello.c \
  -o 00-linux-lab/build/pipeline/hello.s

gcc -c -O0 -g 00-linux-lab/examples/hello.c \
  -o 00-linux-lab/build/pipeline/hello.o

gcc 00-linux-lab/build/pipeline/hello.o \
  -o 00-linux-lab/build/pipeline/hello

file 00-linux-lab/build/pipeline/*
readelf -h 00-linux-lab/build/pipeline/hello
nm 00-linux-lab/build/pipeline/hello.o
```

**Prediction:** `.i/.s` เป็น text; `.o` เป็น relocatable ELF; finalเป็น executable/PIE ELFตาม toolchain default.

**Expected key evidence:** `file` แยก relocatable objectกับ final executable; `readelf`ระบุ x86-64.

**What may vary:** final ELF Type อาจเป็น `DYN` (PIE) หรือ `EXEC`ตาม distro/compiler flags.

**Explain:** gccเป็น driverที่ orchestrate stages; source statementไม่ได้เป็น CPU instructionตรง ๆ.

**Modification:** เพิ่ม `-no-pie` ตอน linkแล้ว compare `readelf -h`.

**Failure mode:** อย่าสับสน sectionใน objectกับ memory mappingของ running process.

**Reflection:** อธิบายสิ่งที่แต่ละ stageเพิ่ม/ลบจาก representationก่อนหน้า.

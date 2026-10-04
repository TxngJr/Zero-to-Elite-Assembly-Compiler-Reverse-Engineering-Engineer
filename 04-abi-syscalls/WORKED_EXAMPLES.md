# Worked Examples — ABI & Linux Syscalls

## Example 1 — First six integer arguments

**Goal:** พิสูจน์ SysV AMD64 calling conventionด้วย C caller + assembly callee.

**Command / action:**

```bash
gcc -g -no-pie \
  04-abi-syscalls/examples/abi_args_test.c \
  04-abi-syscalls/examples/abi_args.s \
  -o /tmp/abi_args

/tmp/abi_args
objdump -d -Mintel /tmp/abi_args | sed -n '/<main>/,/^$/p'
```

**Prediction:** args 1–6ใช้ RDI, RSI, RDX, RCX, R8, R9.

**Expected key evidence:** caller setup registersก่อน call; test resultถูก.

**What may vary:** compilerอาจ reorder temporary loadsแต่ call boundaryต้องตาม ABI.

**Explain:** calling conventionเป็น binary contractคนละเรื่องกับ `call` instruction semantics.

**Modification:** เพิ่ม 7th/8th argumentใน local labแล้ว inspect stack.

**Failure mode:** อย่าคิดว่าทุก architecture/OSใช้ registersชุดนี้.

**Reflection:** วาด stack ณ callee entry.

---

## Example 2 — Callee-saved register

**Goal:** เห็นหน้าที่ของ RBX/RBP/R12–R15.

**Command / action:**

```bash
gcc -g -no-pie \
  04-abi-syscalls/examples/callee_saved_test.c \
  04-abi-syscalls/examples/callee_saved.s \
  -o /tmp/callee_saved

/tmp/callee_saved
objdump -d -Mintel /tmp/callee_saved
```

**Prediction:** assembly functionที่เปลี่ยน callee-saved registerต้อง restoreก่อน return.

**Expected key evidence:** push/popหรือ save/restore equivalent.

**What may vary:** register choiceใน C compiler output.

**Explain:** caller-saved = callerรับผิดชอบถ้าต้องการค่าเดิม; callee-saved = functionที่เปลี่ยนต้องคืนค่า.

**Modification:** intentionally remove restoreใน local copyแล้วให้ testตรวจ corruption จากนั้นคืน fix.

**Failure mode:** อย่าพึ่ง “มันดูเหมือนยังทำงาน” เพราะ callerอาจยังไม่ใช้ registerนั้นใน buildนี้.

**Reflection:** ทำไม ABI testต้องสร้าง callerที่ตรวจ preserved stateโดยตรง?

---

## Example 3 — Raw Linux syscall without libc

**Goal:** แยก function call ABIจาก kernel syscall ABI.

**Command / action:**

```bash
gcc -nostdlib -no-pie \
  04-abi-syscalls/examples/syscall_hello.s \
  -o /tmp/syscall_hello

strace /tmp/syscall_hello
```

**Prediction:** `write` syscallปรากฏใน straceและโปรแกรมจบผ่าน `exit` syscall.

**Expected key evidence:** ไม่มี libc `main` requirement; entryอาจเป็น `_start`; syscall number/argsอยู่ registerตาม Linux x86-64 syscall ABI.

**What may vary:** addresses/strace formatting.

**Explain:** `syscall` instructionเปลี่ยน privilege/modeผ่าน kernel-defined interface; SysV function ABIกับ syscall ABIไม่เหมือนกันทั้งหมด (เช่น arg4).

**Modification:** เปลี่ยน string lengthอย่างถูกต้องแล้วดู `write(fd,buf,count)`.

**Failure mode:** countเกิน buffer lengthอาจทำให้ kernelอ่าน bytesเกิน intended objectใน user address space.

**Reflection:** เปรียบเทียบ R10 vs RCXบทบาทใน syscall/function ABI.

---

## Example 4 — syscall-cat project

**Goal:** ใช้ read/write loopและ error/EOF semantics.

**Command / action:**

```bash
make -C 04-abi-syscalls/projects/syscall-cat clean all
printf 'alpha\nbeta\n' \
  | 04-abi-syscalls/projects/syscall-cat/syscall-cat
```

ถ้าชื่อ artifactต่าง ให้ดู Makefile.

**Prediction:** readคืนจำนวน bytes, 0=EOF, negative=error conventionหลัง syscall.

**Expected key evidence:** outputตรง input.

**What may vary:** read chunk boundaries.

**Explain:** stream semanticsไม่ได้สัญญาว่า readครั้งเดียวได้ข้อมูลทั้งหมด.

**Modification:** feed inputใหญ่กว่า internal bufferแล้วตรวจ loop.

**Failure mode:** hard-codeว่า `read == requested_size` จึงผิด.

**Reflection:** เขียน pseudocode robust read/write loopโดยจัด partial writes.

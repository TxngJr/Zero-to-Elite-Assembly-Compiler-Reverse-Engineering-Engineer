# Course Map

| Chapter | หัวข้อ | ผลลัพธ์หลัก | สถานะ |
|---|---|---|---|
| 00 | Linux Systems Laboratory | ใช้ Fedora/Linux toolchain และตรวจ program/process ได้ | ✅ Implemented |
| 01 | Computer Foundations | เข้าใจ bits, integers, memory และ CPU model | ✅ Implemented |
| 02 | C Machine Model | เชื่อม C กับ bytes, addresses, compiler และ memory | ✅ Implemented |
| 03 | x86-64 Assembly | registers, flags, addressing, control flow | ✅ Implemented |
| 04 | ABI & Linux Syscalls | SysV AMD64 calling convention และ raw syscalls | ✅ Implemented |
| 05 | Computer Architecture | pipeline, cache, VM/TLB, multicore, performance | ✅ Implemented |
| 06 | ELF Internals | headers, sections, segments, symbols, relocations | ✅ Implemented |
| 07 | Linker & Loader | symbol resolution, archives, PIC/PIE, GOT/PLT, loader | ✅ Implemented |
| 08 | Debugging Engineering | GDB, DWARF, signals, core dumps, sanitizers | ✅ Implemented |
| 09 | Compiler Frontend | lexer/parser/AST/type checking | Planned |
| 10 | Intermediate Representation | CFG, data flow, SSA, optimization | Planned |
| 11 | Compiler Backend | instruction selection/register allocation | Planned |
| 12 | Build a Compiler | compiler end-to-end | Planned |
| 13 | OS Foundations | boot, privilege, paging, interrupts | Planned |
| 14 | Build an OS | kernel, memory, scheduler, syscall, FS | Planned |
| 15 | Advanced OS | VM, IPC, SMP, synchronization | Planned |
| 16 | Reverse Engineering | static/dynamic binary analysis | Planned |
| 17 | Defensive Vulnerability Research | sanitizers, fuzzing, crash/root-cause analysis | Planned |
| 18 | Final Capstone | compiler + OS + tooling + RE capstone | Planned |

## Dependency Chain

```text
00 Linux Lab
   ↓
01 Computer Foundations
   ↓
02 C Machine Model
   ↓
03 x86-64 Assembly
   ↓
04 ABI/Syscalls
   ↓
05 Architecture
   ↓
06 ELF → 07 Linker/Loader → 08 Debugging
   ↓                         ↓
09 Frontend → 10 IR → 11 Backend → 12 Compiler
   ↓
13 OS Foundations → 14 Build OS → 15 Advanced OS
   ↓
16 Reverse Engineering → 17 Defensive Research → 18 Capstone
```

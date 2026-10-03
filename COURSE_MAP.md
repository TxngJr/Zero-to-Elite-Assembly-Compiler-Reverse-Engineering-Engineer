# Course Map

| Chapter | Topic | Status |
|---|---|---|
| 00 | Linux Systems Laboratory | ✅ Implemented |
| 01 | Computer Foundations | ✅ Implemented |
| 02 | C Machine Model | ✅ Implemented |
| 03 | x86-64 Assembly | ✅ Implemented |
| 04 | ABI & Linux Syscalls | ✅ Implemented |
| 05 | Computer Architecture | ✅ Implemented |
| 06 | ELF Internals | ✅ Implemented |
| 07 | Linker & Loader | ✅ Implemented |
| 08 | Debugging Engineering | ✅ Implemented |
| 09 | Compiler Frontend | ✅ Implemented |
| 10 | Intermediate Representation | ✅ Implemented |
| 11 | Compiler Backend | ✅ Implemented |
| 12 | My Compiler / EliteC | ✅ Implemented |
| 13 | OS Foundations | ✅ Implemented |
| 14 | My OS / EliteOS64 | ✅ Implemented |
| 15 | Advanced OS | ✅ Implemented |
| 16 | Reverse Engineering | ✅ Implemented |
| 17 | Defensive Security Lab | ✅ Implemented |
| 18 | Final Capstone | ✅ Implemented |

## Dependency chain

```text
00 Linux → 01 Foundations → 02 C
→ 03 Assembly → 04 ABI/Syscalls → 05 Architecture
→ 06 ELF → 07 Linker/Loader → 08 Debugging
→ 09 Frontend → 10 IR → 11 Backend → 12 EliteC
→ 13 OS Foundations → 14 EliteOS64 → 15 Advanced OS
→ 16 Reverse Engineering → 17 Defensive Security
→ 18 Final Capstone
```

## Completion

The implementation roadmap is complete at Chapter 18. Further work belongs to extension tracks such as full SSA/register allocation, user-mode EliteOS integration, VFS/filesystems, APIC/SMP, richer RE tooling and extended defensive fuzzing.

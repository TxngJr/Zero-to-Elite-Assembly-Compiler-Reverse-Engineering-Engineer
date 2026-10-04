# Course Map

| Chapter | Topic | Repository status |
|---|---|---|
| 00 | Linux Systems Laboratory | Educational implementation + mastery rubric |
| 01 | Computer Foundations | Educational implementation + mastery rubric |
| 02 | C Machine Model | Educational implementation + mastery rubric |
| 03 | x86-64 Assembly | Educational implementation + mastery rubric |
| 04 | ABI & Linux Syscalls | Educational implementation + mastery rubric |
| 05 | Computer Architecture | Educational implementation + mastery rubric |
| 06 | ELF Internals | Educational implementation + mastery rubric |
| 07 | Linker & Loader | Educational implementation + mastery rubric |
| 08 | Debugging Engineering | Educational implementation + mastery rubric |
| 09 | Compiler Frontend | Tested educational implementation |
| 10 | IR / data-flow / SSA construction | Tested educational implementation |
| 11 | x86-64 backend + allocator lab | Baseline backend + separate linear-scan lab |
| 12 | EliteC Integration | Tested educational compiler |
| 13 | OS Foundations | Models / exercises |
| 14 | EliteOS64 | Kernel implementation + separate QEMU runtime gate |
| 15 | Advanced OS Models | Host-side models; not kernel-integrated |
| 16 | Reverse Engineering | Authorized course tooling/challenges |
| 17 | Defensive Security | Course-owned defensive labs |
| 18 | Capstone | Automated baseline + learner-created assignment |

## Important boundaries

- “Automated checks pass” ≠ learner mastery.
- Chapter 15 models ≠ EliteOS64 process/VFS/syscall implementation.
- Linear-scan lab ≠ allocator integrated into generated EliteC code.
- Sanitizer/fuzzer clean runs ≠ security proof.
- QEMU boot ≠ universal hardware compatibility.

## Long-term extension tracks

The course intentionally exposes next steps rather than claiming production completeness:
- integrate SSA-based optimization into backend
- integrate register allocation into codegen
- richer language types/runtime/object emission/DWARF
- ring3 + VMM + scheduler + syscalls + VFS in EliteOS64
- APIC/SMP
- deeper RE/decompiler workflows
- longer coverage-guided fuzz campaigns

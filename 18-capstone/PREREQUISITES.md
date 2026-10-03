# Prerequisites

Capstone assumes Chapters 00–17 are complete.

Minimum readiness:

- can read x86-64 assembly without translating every instruction to C
- understands SysV AMD64 calling convention
- can inspect ELF with readelf/objdump/nm
- understands GDB register/memory workflow
- understands compiler frontend→IR→backend pipeline
- understands page tables, interrupts and freestanding kernels
- understands process/COW/scheduler/VFS concepts
- can reverse engineer course-owned binaries using evidence
- can use ASan/UBSan and regression/fuzz tests defensively

Run the full verifier before beginning:

```bash
../scripts/verify-chapters.sh
```

Do **not** make the capstone runner invoke that root verifier internally; the root verifier itself runs Chapter 18 and recursive invocation would loop.

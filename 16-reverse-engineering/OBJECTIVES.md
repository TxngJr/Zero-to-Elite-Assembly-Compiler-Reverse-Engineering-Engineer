# Objectives

เมื่อจบบทนี้ควรสามารถ:

- establish binary provenance/hashก่อน analysis
- classify ELF type/architecture/PIE/stripped status
- read sections/segments/symbol tables/dynamic dependencies
- identify compiler-generated function boundariesเมื่อ symbolsมี
- reason about stripped binariesโดยใช้ calls/control flow/data references
- recognize common x86-64 function/loop/branch/switch patterns
- distinguish source constructs from compiler transformations
- reconstruct structs/arraysจาก offsets/stridesอย่างระมัดระวัง
- analyze optimized binariesโดยไม่คาด source↔assembly 1:1
- identify RIP-relative data accesses
- use GDBกับ course binaries for register/memory observation
- build a control-flow edge summaryจาก disassembly
- compare O0/O2/PIE/stripped variants
- write an evidence-based RE reportที่แยก facts, hypothesesและ uncertainty

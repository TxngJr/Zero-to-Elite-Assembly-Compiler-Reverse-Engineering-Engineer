# Common Mistakes

- ISA = CPU implementationภายในทั้งหมด
- Fetch→Decode→Executeคือ timingจริงของ modern x86
- GHz = instructions per secondโดยตรง
- pipelineลด latencyของ instructionเดี่ยวเสมอ
- branchlessเร็วกว่า branchเสมอ
- cache line sizeเป็น language/ISA universal constant
- TLB miss = page fault
- virtual address = physical address
- cache coherence = full memory consistency
- volatile = atomic/synchronization
- row-majorเร็วกว่า column-majorทุก measurementโดยไม่ดู noise
- performance resultหนึ่งครั้ง = proof
- optimizeก่อน profile/correctness

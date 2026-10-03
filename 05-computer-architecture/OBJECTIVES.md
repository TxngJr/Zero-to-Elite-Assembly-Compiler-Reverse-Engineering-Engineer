# Objectives

เมื่อจบบทนี้ควรสามารถ:
- แยก ISA ออกจาก microarchitecture
- อธิบาย datapath, control, register file, ALU และ program counterแบบ simplified
- อธิบาย pipeline stages และ RAW/control/structural hazards
- อธิบาย forwarding, stalls, flushes และ branch prediction
- อธิบาย superscalar, out-of-order, register renaming และ reorder bufferเชิงแนวคิด
- คำนวณ cache offset/index/tag สำหรับ direct-mapped cache
- อธิบาย temporal/spatial locality, cache miss types และ write policies
- อธิบาย virtual address, page table, TLB, page fault และ MMU
- แยก interrupts, exceptions, faults และ syscallsระดับ concept
- อธิบาย multicore coherence vs consistencyแบบไม่ปนกัน
- reason เรื่อง latency, throughput, CPI/IPC และ Amdahl's Law
- ใช้ tiny CPU/cache/branch simulatorsเพื่อพิสูจน์ mental model

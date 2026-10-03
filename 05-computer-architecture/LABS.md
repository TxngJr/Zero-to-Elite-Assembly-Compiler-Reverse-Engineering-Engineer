# Labs

1. **ISA vs uarch inventory:** จาก `lscpu` แยกสิ่งที่เป็น architecture/feature observationออกจาก language rule.
2. **Tiny datapath paper trace:** trace PC/register/ALU/memoryสำหรับ fictional instructions.
3. **Tiny CPU simulator:** เพิ่ม SUB/JZ programและ trace stateทุก step.
4. **RAW hazard:** วาด 5-stage timingของ ADD→dependent ADD; ใส่ forwarding/stallตาม assumptions.
5. **Load-use:** เปรียบเทียบกรณี forwardingอย่างเดียวพอ/ไม่พอใน simplified pipeline.
6. **Branch flush:** วาด instructionsที่ต้อง squashเมื่อ branch resolve late.
7. **2-bit predictor:** feed TTTT, TNTN, loop-like pattern; trace state transitions.
8. **Locality:** run `locality.c` หลายรอบ; ห้าม assertว่า rowต้องเร็วกว่าทุกครั้ง—อธิบาย noise.
9. **Cache split:** cache-sim direct-mapped; คำนวณ tag/index/offsetของ traceด้วยมือ.
10. **Conflict miss:** สร้าง addressesที่ชน indexเดียวกันและสังเกต thrashing.
11. **Associativity design:** บนกระดาษแปลง direct-mapped simulatorเป็น 2-way LRU.
12. **Page math:** สำหรับ 4 KiB pages แยก offset/VPNของ virtual addressesหลายค่า.
13. **TLB vs page fault:** classify scenariosว่า TLB hit/miss/page fault.
14. **False sharing thought experiment:** สอง countersใน lineเดียว vsแยก line; อธิบาย coherence trafficโดยไม่อ้าง speedupก่อนวัด.
15. **perf optional:** `perf stat` กับ locality/branch examplesถ้า Fedoraอนุญาต; compare instructions, branches, branch-misses, cache metricsที่ available.

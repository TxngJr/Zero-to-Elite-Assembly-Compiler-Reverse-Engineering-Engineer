# Theory — Computer Architecture

## 1. Abstraction layers

```text
C / source language
      ↓
Compiler
      ↓
ISA instructions (x86-64)
      ↓
Microarchitecture
      ↓
Digital logic / circuits
      ↓
Physical devices
```

ISAบอก programmer-visible behavior; microarchitectureเลือกวิธี implement behaviorนั้น.

## 2. Architectural state
Programmer-visible stateเช่น general registers, RIP, RFLAGS และ memory modelตาม ISA. Cache lines, reorder buffer entries หรือ predictor stateส่วนใหญ่ไม่ใช่ architectural stateแม้มีผลต่อ performance.

## 3. Datapath/control simplified
CPU modelพื้นฐานมี program counter, instruction memory/interface, register file, ALU, data memory/interface และ control logic. จริง x86 decodeซับซ้อนกว่านี้มากและอาจ translateเป็น internal micro-ops.

## 4. Sequential logic and clock
Combinational logicคำนวณ outputจาก current inputs; state elementsเก็บค่า across cycles. Clockใช้ coordinate state updatesใน synchronous designs แต่ modern CPUมีรายละเอียดหลาย clock domains/pipelines.

## 5. Simplified instruction cycle
Fetch → Decode → Execute → Memory → Writeback เป็น teaching modelที่เหมาะกับ RISC-like pipeline. x86 implementationsอาจมี front-end decode/uop cache, rename, schedule, multiple execution unitsและ retire stages.

## 6. Pipeline
Pipeline overlapหลาย instructions. ถ้ามี 5 stages การมี instructionหนึ่ง “ครบใน 5 cycles” ไม่ได้แปล throughputหนึ่ง instructionต่อ 5 cyclesหลัง pipelineเต็ม.

## 7. Hazards
- **RAW** read-after-write: consumerต้องรอ producer
- **WAR/WAW:** สำคัญใน out-of-order/name dependency contexts
- **structural:** resourceชนกัน
- **control:** next PCไม่แน่เพราะ branch

In-order teaching pipelineมัก focus RAW + control + structural.

## 8. Forwarding and stalls
Forwarding/bypassingส่ง resultจาก stageหนึ่งไป consumerก่อน writeback. ถ้า dataยังไม่พร้อมต้อง stall/bubble. Load-use hazardเป็นตัวอย่างคลาสสิก.

## 9. Branch prediction
CPUเดา branch direction/targetเพื่อ fetchต่อ. เดาถูกช่วยให้ pipelineเดิน; เดาผิดต้อง discard speculative workและ redirect. Predictorจริงมี stateซับซ้อนมากกว่า 1-bit/2-bit modelsใน project.

## 10. Speculation
Speculative executionทำงานก่อนรู้ว่าจะ commitจริงหรือไม่. Architectural stateต้องปรากฏเหมือน executionที่ถูกต้องเมื่อ retire; microarchitectural side effectsอาจมีรายละเอียดด้าน performance/security ซึ่งเราจะไม่ใช้เพื่อสร้าง exploitในบทนี้.

## 11. Superscalar
CPU superscalar issue/executeมากกว่าหนึ่ง operationต่อ cycleเมื่อ dependencies/resourcesเอื้อ. “Clock 4 GHz = 4 billion instructions/s” จึงไม่ถูกทั่วไป.

## 12. Out-of-order execution
Instructionsสามารถ executeไม่ตาม program orderเมื่อ operandsพร้อม แต่ retire/commitอย่างควบคุมเพื่อรักษา precise architectural behavior. Structuresเช่น reservation stations/schedulers และ reorder bufferเป็น mental modelสำคัญ.

## 13. Register renaming
Rename mapping architectural registersไป physical registersเพื่อลด false dependenciesเช่น WAR/WAW. RAW true dependencyยังคงอยู่.

## 14. Memory hierarchy

```text
registers
L1 cache
L2 cache
L3 / LLC
DRAM
storage
```

ยิ่งใกล้ coreมักเร็ว/เล็ก/แพงต่อ byteกว่า. Exact sizes/latenciesขึ้นกับ CPU.

## 15. Locality
- temporal locality: ใช้ข้อมูลเดิมซ้ำเร็ว ๆ
- spatial locality: ใช้ addressesใกล้กัน

Row-major traversalของ C arrayมักใช้ spatial localityดีกว่า column strideใหญ่ แต่ compiler/prefetch/cache geometryทำให้ measured resultต้องตรวจจริง.

## 16. Cache lines
Cachesเคลื่อนข้อมูลเป็น blocks/cache lines ไม่ใช่ทีละ C variable. Common x86 CPUsจำนวนมากใช้ 64-byte linesแต่ไม่ควรอ้างเป็น universal ISA guarantee.

## 17. Direct-mapped address split
สำหรับ cacheที่ block size = 2^b และ lines = 2^s:

```text
address = [ tag | index(s bits) | offset(b bits) ]
```

offsetเลือก byteใน block; indexเลือก line; tagแยก blocksที่ชน indexเดียวกัน.

## 18. Set associative
N-way set associativeมีหลาย linesต่อ set. Addressเลือก setหนึ่ง แล้ว compare tagกับ N ways. Fully associative = หนึ่ง setหลาย entries.

## 19. Miss categories
Compulsory/cold, capacity, conflict เป็น classic 3C model. Multicore/coherenceยังมี missesจาก invalidation/communicationที่ modelง่ายนี้ไม่ครอบคลุม.

## 20. Write policies
Write-throughเขียน lower levelด้วย; write-back mark dirtyแล้วเขียนเมื่อ evict. Write-allocate/no-write-allocateกำหนด behaviorของ store miss. Designจริงขึ้นกับ cache level.

## 21. Prefetching
Hardware/software prefetchพยายามนำข้อมูลมาก่อน demand. ช่วย sequential patternsแต่ทำให้ bandwidth/cache pollutionแย่ได้ถ้าเดาผิด.

## 22. Virtual memory
Processใช้ virtual addresses. MMUแปล VA→PAตาม page tables. Mappingอาจไม่มี, read-only, non-executable หรือชี้ physical frameร่วมกัน.

## 23. Pages
Pageเป็น fixed-size translation granuleตาม mode/config; 4 KiBเป็น common base pageบน x86-64 Linux แต่ยังมี huge pages. Page offsetไม่ต้อง translate; upper VPNใช้ page-table lookup.

## 24. TLB
TLB cache translations. TLB hitหลีกเลี่ยง page-table walk; missไม่จำเป็นต้องเป็น page fault—hardware/softwareอาจ walk page tablesแล้วเติม TLB.

## 25. Page faults
Faultเกิดเมื่อ translation/permissionต้องการ OS intervention เช่น demand paging, COW หรือ invalid access. บาง faultถูกแก้แล้ว instruction retry; invalid accessอาจนำไป signal.

## 26. Protection
Page permissionsเช่น read/write/executeและ user/supervisorช่วย isolation. NX/XDช่วย mark pages non-executable. Permissionsเป็นส่วนหนึ่งของ memory protection modelไม่ใช่เพียง performance.

## 27. Exceptions/interrupts/syscalls
Exceptionสัมพันธ์กับ current instruction (เช่น page fault/divide error); interruptมาจาก asynchronous eventโดยทั่วไป; syscallเป็น deliberate controlled transitionจาก userไป kernel. Exact terminology/type classificationขึ้นกับ architecture docs.

## 28. Multicore caches and coherence
แต่ละ coreอาจมี private caches. Coherence protocolทำให้ coresเห็น single-memory-location writesอย่างสอดคล้องในระดับ protocol; MESI-like statesเป็น common teaching modelแต่ implementationจริงอาจต่าง.

## 29. Coherence vs consistency
**Coherence** เน้น ordering/visibilityของ writesต่อ locationเดียว. **Memory consistency model** กำหนด permitted ordering/visibilityข้าม multiple memory operations/locations. อย่าปนคำสองคำนี้.

## 30. Atomics and synchronization
Atomic read-modify-write, fences และ locksสร้าง inter-thread orderingตาม language/ISA model. `volatile` จาก Chapter 02ไม่แทน atomics.

## 31. False sharing
Threadsเขียนคนละ variablesแต่ variablesอยู่ cache lineเดียวกัน อาจเกิด coherence trafficหนักแม้ไม่ได้แชร์ logical variableเดียว. Padding/alignmentอาจช่วยแต่ต้องวัดและพิจารณา memory cost.

## 32. Latency vs throughput
Latency = เวลาของ operationหนึ่งจนเสร็จ; throughput = rateที่ระบบรับ/เสร็จ operationsต่อเวลา. Pipeline/parallel unitsทำให้สองค่าไม่เหมือนกัน.

## 33. CPI and IPC
CPI = cycles/instruction; IPC = instructions/cycle. ทั้งคู่ขึ้นกับ workload, instruction mix, cache misses, branch mispredictsและ core width. x86 variable instructions/uopsทำให้ interpretationต้องระวัง.

## 34. Amdahl's Law
ถ้า fraction P เร่งได้ factor S:

```text
Speedup = 1 / ((1-P) + P/S)
```

ส่วนที่เร่งไม่ได้จำกัด overall speedup.

## 35. Measurement
Wall-clock timingถูกรบกวนโดย scheduler, DVFS/turbo, caches, background load. ใช้ repeated runs, warmup, sufficient workload และ toolsอย่าง `perf stat` เมื่อมีสิทธิ์. Measurementหนึ่งครั้งไม่ใช่ proof.

## 36. Reading performance responsibly
อย่า optimizeจาก intuitionอย่างเดียว. ดู correctnessก่อน แล้ว profileเพื่อหา bottleneck. Compiler optimizationsและ CPU generationเปลี่ยนผลได้มาก.

# Theory — Advanced Operating Systems

## 1. From Kernel to Multi-Process OS

Chapter 14มี kernelหนึ่ง address spaceและทุก codeอยู่ ring0. Advanced OSต้องเพิ่ม:

```text
isolation + scheduling + system-call boundary + files/IPC + concurrency
```

## 2. Process vs Thread

**Process**โดยทั่วไปคือ resource container + address space + handles/credentials.  
**Thread**คือ schedulable execution contextภายใน process.

หนึ่ง processมีหลาย threadsได้.

## 3. Execution Context

Context switchอาจต้องเก็บ:
- general-purpose registers
- RIP/RSP/RFLAGS
- SIMD/FPU stateเมื่อใช้งาน
- kernel stack pointer
- address-space root (CR3) เมื่อสลับ process
- thread-local/per-CPU metadata

ต้องกำหนด contractชัดว่า registerใดถูก saveที่ไหน.

## 4. Kernel Stacks

แต่ละ threadควรมี kernel stackของตัวเอง. เมื่อ user→kernel transition hardware/kernelต้องเปลี่ยนจาก user RSPไป privileged stackอย่างปลอดภัย.

## 5. TSS and RSP0

x86-64 TSSใช้เก็บ RSP0/RSP1/RSP2 และ IST stack pointers. OSทั่วไปใช้ RSP0เป็น ring3→ring0 stack target.

## 6. IST

Interrupt Stack Tableช่วยให้ critical exceptionsเช่น double faultใช้ known-good stackแม้ current stackเสีย.

## 7. Robust Exception Stubs

เพราะบาง exceptions push error codeและบางอันไม่ push, stubsมัก normalize frame:

```text
vector + synthetic/real error code + saved registers + hardware frame
```

จากนั้น C handlerอ่าน structureที่ predictable.

## 8. User Mode

ก่อน `iretq`เข้าสู่ ring3ต้องมี:
- user code/data GDT entries
- user-accessible page mappings
- user RIP/RSP
- controlled RFLAGS
- TSS RSP0
- syscall/interrupt entry pathกลับ kernel

## 9. Address Spaces

Processหนึ่งมักมี top-level page tableของตัวเอง. Kernel mappingsอาจถูก shareใน high half ขณะที่ user mappingsต่างกัน.

CR3 switchเปลี่ยน address spaceและมี TLB implications.

## 10. Page Fault as a Mechanism

Page faultไม่ใช่แค่ crash; OSใช้ทำ:
- demand paging
- copy-on-write
- stack growthตาม policy
- memory-mapped files

Handlerต้องแยก valid recoverable faultจาก invalid access.

## 11. fork()

Conceptually `fork`สร้าง childที่เริ่มด้วย memory imageเหมือน parent. Copyทุก pageทันทีแพง จึงนิยมใช้ copy-on-write.

## 12. Copy-on-Write

fork:
1. parent/childชี้ physical framesเดียวกัน
2. mappingsเป็น read-only COW
3. increment frame refcount

write fault:
1. ถ้า shared refcount > 1 → allocate frameใหม่ + copy + decrement old ref
2. map writerเป็น writable
3. resume faulting instruction

## 13. Frame Reference Counts

COWต้องรู้ frameถูก shareกี่ mappings. Refcount 0 → frameคืน PMMได้. Overflow/underflowคือ correctness bugsร้ายแรง.

## 14. Scheduler

Schedulerเลือก runnable threadถัดไป.

Inputs:
- task states
- priority/policy
- CPU affinity
- time slice
- blocking/wakeup events

## 15. Round Robin

Round-robinใช้ ready queueและ time quantumเท่ากันโดยพื้นฐาน. Fair/easy แต่ไม่ optimize latency/priorityทุก workload.

## 16. Preemption

Timer interruptสามารถ mark current taskให้ reschedule. Actual switchควรเกิดใน controlled pathที่ register/stack stateครบ.

## 17. Task States

Typical:
- RUNNING
- READY
- BLOCKED/SLEEPING
- TERMINATED

Blocked taskไม่ควรถูก schedulerเลือกจน eventทำให้ READY.

## 18. Context-Switch Boundary

อย่าสลับ contextกลาง C functionแบบไม่มี contract. Kernelsออกแบบ switch assembly routineและ stack layoutอย่างเจาะจง.

## 19. System Calls

Syscall boundaryรับ untrusted user arguments. Kernelต้อง:
- validate syscall number
- validate pointers/ranges
- copy dataอย่างปลอดภัย
- check permissions/handles
- return controlled errors

## 20. SYSCALL/SYSRET Preview

x86-64มี `syscall/sysret` และ MSRsกำหนด entry/segments. `sysret`มี canonical-address/flags caveats จึงต้อง implementตาม architecture manualอย่างระวัง.

## 21. User Pointers

Kernelไม่ควร dereference arbitrary user pointerแบบ blind. ต้อง validate mapping/rangeและจัดการ page faults/TOCTOUตาม design.

## 22. Handles / File Descriptors

User processถือ small integer handle; kernel table mapไป object. สิ่งนี้ช่วยควบคุม lifetime/permissionsแทน expose kernel pointer.

## 23. IPC

Inter-process communication options:
- pipes
- message queues
- shared memory
- sockets
- signals/events

แต่ละแบบมี buffering/blocking/lifetime semantics.

## 24. Pipe

Bounded pipeมี circular buffer + read/write indices. เมื่อ empty readerอาจ block; เมื่อ full writerอาจ blockหรือ return partialตาม API.

Simulatorบทนี้เน้น ring-buffer semanticsก่อน scheduler blocking integration.

## 25. VFS

Virtual File Systemให้ common interfaceเหนือหลาย filesystem/device backends.

Common objects:
- inode/vnode — underlying file object metadata
- dentry/name cache — path component resolution
- file/open description — offset/flags/session state

## 26. Path Resolution

`/a/b/c`:
1. start root
2. lookup `a`
3. require directory
4. lookup `b`
5. continue

Real VFSต้องจัด symlinks, mount points, `.`, `..`, permissions, races.

## 27. File Offset

Open file descriptionเก็บ current offset. Multiple descriptorsอาจ shareหรือไม่ share offsetขึ้นกับ duplication semantics.

## 28. Synchronization

Interrupts + SMPทำให้ shared stateมี races.

Tools:
- atomics
- spinlocks
- mutexes
- condition/wait queues
- interrupt masking (limited scope)

## 29. Spinlock

เหมาะ critical sectionสั้นเมื่อ threadไม่สามารถ sleep. บน SMPต้องใช้ atomic acquire/release semantics.

## 30. Mutex

Mutexอนุญาต sleeping/blockingรอ ownership เหมาะ critical sectionยาวกว่า แต่ต้องมี scheduler.

## 31. Deadlock

Classic conditions:
- mutual exclusion
- hold and wait
- no preemption
- circular wait

Lock orderingเป็นวิธีป้องกันสำคัญ.

## 32. Memory Ordering

Compiler/CPU reorderบาง operations. Correct concurrent codeต้องใช้ atomics/fences/lock primitivesตาม memory model—not `volatile`.

## 33. Per-CPU Data

ลด contentionโดยเก็บ counters/queuesต่อ CPU. ต้องระวัง migrationและ aggregation.

## 34. APIC / IOAPIC

Modern SMP OSใช้ Local APICต่อ coreและ IOAPIC/MSIสำหรับ devicesแทน legacy PIC.

## 35. SMP Startup

Secondary cores (APs)ต้องถูก bootstrap, ให้ stack/per-CPU stateและเข้าสู่ scheduler. รายละเอียด hardware-specificและเป็น challengeระดับสูง.

## 36. TLB Shootdown

เมื่อ CPUหนึ่งเปลี่ยน page tableที่ coreอื่นกำลัง cache translation ต้อง coordinate invalidationผ่าน inter-processor interruptsหรือ mechanismที่เหมาะ.

## 37. VFS Cache / Page Cache

Production OS cache file data/pagesและ metadata. Coherencyกับ mmap/writebackเพิ่ม complexityมาก.

## 38. Signals / Events

Asynchronous notificationsต้อง define delivery points, saved context, masks และ restart semantics.

## 39. Security Boundary

User/kernel isolationพึ่ง:
- page permissions
- privilege level
- validated syscalls
- object permissions
- safe copyin/copyout
- resource accounting

Bugใน boundaryอาจกลายเป็น kernel compromise จึงต้อง minimalและ testable.

## 40. Integration Order for EliteOS64

Recommended:
1. robust exception frames
2. 4 KiB page mapper
3. bitmap PMM
4. TSS + user GDT
5. user-mode test task
6. context-switch primitive
7. scheduler
8. syscall entry
9. process table/handles
10. pipe/VFS
11. APIC/SMP

อย่าพยายามเพิ่มทุก subsystemพร้อมกัน.

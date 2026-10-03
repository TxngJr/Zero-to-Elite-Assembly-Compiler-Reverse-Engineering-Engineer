# Objectives

เมื่อจบบทนี้ควรสามารถ:

- อธิบาย robust exception-frame designบน x86-64
- อธิบาย TSS, RSP0 และ IST
- อธิบาย ring3 transitionและ user/kernel stacks
- แยก process, thread, address space และ execution context
- อธิบาย context switch state
- อธิบาย preemptive vs cooperative scheduling
- implement round-robin scheduler simulator
- อธิบาย per-process page tables
- อธิบาย forkและ copy-on-write
- implement COW simulatorพร้อม frame reference counting
- อธิบาย syscall dispatchและ validation boundary
- อธิบาย IPC pipe buffering/blockingภาพรวม
- implement bounded pipe simulator
- อธิบาย VFS inode/dentry/file concepts
- implement path lookupใน in-memory VFS
- อธิบาย spinlock/mutex/atomic/fence distinctions
- อธิบาย SMP, APIC/IOAPIC และ per-CPU data concepts
- วางแผน integrationจาก simulatorกลับเข้าสู่ EliteOS64อย่างเป็นลำดับ

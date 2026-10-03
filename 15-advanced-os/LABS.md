# Labs

1. วาด normalized exception frameทั้ง vectorที่มี/ไม่มี error code.
2. วาด user→kernel stack transitionผ่าน TSS RSP0.
3. ระบุ stateที่ context switchต้องเก็บ.
4. Run scheduler-simและ trace ready queue.
5. เปลี่ยน quantum 1/2/4แล้วอธิบาย schedule.
6. เพิ่ม BLOCKED stateใน local scheduler copy.
7. Run vm-cow-sim demo; ดู parent/child share frame.
8. Trigger child writeแล้วดู refcountsเปลี่ยน.
9. อธิบาย page-fault bitsที่ COW handlerต้องตรวจ.
10. ออกแบบ CR3 switch flow.
11. วาด syscall dispatch table.
12. ออกแบบ safe user-pointer validation checklist.
13. Run ipc-sim; trace head/tail/count.
14. ทดลอง pipe full/empty edge cases.
15. Run vfs-sim path lookup.
16. เพิ่ม nested fileใน local VFS tree.
17. อธิบาย inode vs open-file object.
18. วาด lock orderingสอง locksเพื่อหลีกเลี่ยง deadlock.
19. อธิบาย TLB shootdown scenarioสอง cores.
20. เขียน EliteOS64 integration roadmapโดยรักษา boot milestoneทุกขั้น.

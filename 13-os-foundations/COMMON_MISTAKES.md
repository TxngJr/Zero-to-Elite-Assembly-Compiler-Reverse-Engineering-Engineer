# Common Mistakes

- kernelมี libcให้ใช้โดยอัตโนมัติ
- firmware = bootloader
- Multiboot2 = UEFI
- เปิด pagingก่อน page tablesพร้อม
- CR3เก็บ virtual addressของ PML4
- long modeแล้ว GDTไม่สำคัญเลย
- exception = hardware IRQเสมอ
- TLB miss = page fault
- PMM = heap allocator
- virtual address = physical addressเพราะ early kernel identity-map
- volatile = interrupt synchronizationครบถ้วน
- QEMU bootได้ = hardwareทุกเครื่องต้อง bootได้

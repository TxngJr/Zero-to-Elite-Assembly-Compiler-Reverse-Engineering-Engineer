# Challenges

- **08-A First Bad Write:** ใช้ watchpointหา writeแรกที่ทำ Inventory.countเกิน capacityใน injected-bug build.
- **08-B Optimized Mystery:** `-O2 -g`; reconstructค่าจาก registers/memoryแม้ local optimized out.
- **08-C Post-mortem Report:** course crash → evidence → root cause → patch → regression.
- **08-D Loader Breakpoints:** main + shared function + syscall boundaryใน course app แล้ววาด transitions.
- **08-E Batch Debug CI:** GDB batch scriptตรวจ breakpoint hitและ invariantโดย exit nonzeroเมื่อผิด.

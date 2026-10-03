# Challenges

- **14-A CPUID Guard:** ตรวจ CPUID/long-mode supportก่อนเปิด pagingและ print error checkpoint.
- **14-B Exception Framework:** แยก stubsที่มี/ไม่มี error codeแล้วส่ง normalized frameไป C.
- **14-C Bitmap PMM:** เปลี่ยน bump allocatorเป็น bitmapที่ free/reuse framesได้.
- **14-D 4 KiB VMM:** เพิ่ม `map_page/unmap_page` หลัง early huge-page bootstrap.
- **14-E QEMU GDB:** bootด้วย `-s -S`, connect GDB, break `kernel_main`, inspect CR3/page tables.

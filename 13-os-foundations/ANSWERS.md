# Answers and Hints

- 48-bit paging indices: 9+9+9+9 bits + 12-bit offset.
- 4 KiB page offset = 12 bits.
- CR3ชี้ physical addressของ top-level table.
- TLB missอาจ page-walkสำเร็จโดยไม่มี page fault.
- PMMจัด physical frames; VMMจัด mappings; heapจัด variable-size allocations.
- Multiboot2เป็น boot protocol ไม่ใช่ firmware API.
- Chapter14ใช้ huge pagesช่วง bootเพื่อลดจำนวน page tables.
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

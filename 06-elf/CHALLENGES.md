# Challenges

- **06-A ELF Header Decoder:** decode headerเองก่อน cross-check readelf.
- **06-B VA → File Offset:** จาก program headers หา file-backed byteของ VAหรือพิสูจน์ว่าไม่มี.
- **06-C Section/Symbol Browser:** ขยาย inspectorให้เลือก sectionและ list GLOBAL symbols.
- **06-D Corruption Suite:** แก้ magic/class/table offsetsใน copiesของ course ELF; parserต้อง reject safely.
- **06-E BSS Experiment:** สร้าง .bss ≥16 MiB แล้วอธิบาย file size, memsz และ demand paging.

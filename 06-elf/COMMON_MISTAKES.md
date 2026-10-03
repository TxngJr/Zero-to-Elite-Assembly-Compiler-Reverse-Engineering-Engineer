# Common Mistakes

- ELF = executableอย่างเดียว
- ET_DYN = shared libraryเสมอ
- section = segment
- loader mapทุก sectionทีละอัน
- e_entry = main
- e_entryเป็น file offset
- .bss zerosทั้งหมดอยู่ใน file
- .symtabจำเป็นต่อ runtime
- stripped binaryไม่มี symbolsใดเลย
- undefined symbolใน .o = objectเสีย
- relocation = dynamic linkingเท่านั้น
- เชื่อ offsetsจาก untrusted fileโดยไม่ bounds-check

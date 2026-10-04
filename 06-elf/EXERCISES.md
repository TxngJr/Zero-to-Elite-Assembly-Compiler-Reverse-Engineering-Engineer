# Exercises

## วิธีทำแบบฝึกหัดชุดนี้

ทุก numbered prompt ต้องตอบ 4 ส่วน: **Explain**, **Concrete example**, **Evidence**, และ **Boundary / misconception**. โจทย์คำนวณ/assembly/CFG ต้องแสดงขั้นตอน; โจทย์ code ต้องมี test/evidence.


1. ELF magicคืออะไร
2. ELFCLASS64บอกอะไร
3. endianness fieldสำคัญอย่างไร
4. ET_REL/ET_EXEC/ET_DYN/ET_COREต่างกัน
5. PIEมัก typeใด
6. e_entryเป็น offsetหรือ VA
7. e_phoffคืออะไร
8. e_shoffคืออะไร
9. program header vs section header
10. PT_LOADหน้าที่
11. p_filesz vs p_memsz
12. ทำไม p_memszใหญ่กว่าได้
13. p_flags
14. PT_INTERP
15. PT_DYNAMIC
16. .text
17. .rodata
18. .data
19. .bss
20. SHT_NOBITS
21. sh_name pointerหรือ offset
22. e_shstrndx
23. .symtab vs .dynsym
24. .strtab vs .dynstr
25. LOCAL/GLOBAL/WEAK
26. FUNC/OBJECT
27. UNDใน .o เป็น errorทันทีไหม
28. relocationแก้ปัญหาอะไร
29. S/A/P
30. PC-relative vs absolute
31. file offset vs VA
32. mainเป็น entryเสมอไหม
33. stripเอาอะไรออกได้
34. debug sectionsจำเป็นต่อ loaderไหม
35. readelf -l
36. readelf -S
37. readelf -s
38. readelf -r
39. readelf -d
40. objdump -dr
41. nm -u
42. size
43. ทำไม header rangesต้อง bounds-check
44. integer overflowทำ parserพังอย่างไร
45. string tableต้องตรวจ NULเพราะอะไร
46. ET_DYN=libraryเสมอไหม
47. segment alignmentเกี่ยวกับ mappingอย่างไร
48. GNU_STACK
49. GNU_RELRO
50. สร้าง checklistวิเคราะห์ ELF 8 ข้อ

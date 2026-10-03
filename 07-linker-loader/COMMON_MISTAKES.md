# Common Mistakes

- linker = loader
- compileสำเร็จแปลว่า symbols resolveแล้ว
- archiveทุก memberถูก copyเข้า executableเสมอ
- -fPIC = shared libraryเอง
- GOT = PLT
- DT_NEEDEDเป็น absolute pathเสมอ
- SONAME = filenameเสมอ
- LD_LIBRARY_PATH=. เป็น permanent fixทุกปัญหา
- lddเหมาะกับไฟล์ไม่รู้จักทุกกรณี
- PIE = shared library
- dynamic loader = libc
- constructor = ELF entry point

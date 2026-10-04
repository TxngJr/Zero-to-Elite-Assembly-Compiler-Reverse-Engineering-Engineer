# Answers and Hints

- linkerทำ resolution/layout/relocationsตอน build; loaderทำ runtime mappings/resolution
- archive extractionโดยทั่วไป demand-drivenจาก unresolved symbols
- ABS toy = `S+A`; PC-relative toy = `S+A-P`
- GOTเก็บ indirection/address data; PLTเป็น call stub mechanism
- `$ORIGIN` ต้อง quoteเพื่อให้ tokenถึง linker/loader
- missing library: เริ่มจาก `readelf -d`, SONAME/RUNPATH/search rules—not copy .soสุ่มเข้า system dirs
## วิธีใช้ Answers/Hints

ไฟล์นี้เป็น selected hints. Worked solutions อยู่ใน [WORKED_EXAMPLES.md](WORKED_EXAMPLES.md). ทุก exercise ต้องมี explanation + example + evidence + misconception และให้คะแนนด้วย [RUBRIC.md](RUBRIC.md).

# Answers and Hints

- linkerทำ resolution/layout/relocationsตอน build; loaderทำ runtime mappings/resolution
- archive extractionโดยทั่วไป demand-drivenจาก unresolved symbols
- ABS toy = `S+A`; PC-relative toy = `S+A-P`
- GOTเก็บ indirection/address data; PLTเป็น call stub mechanism
- `$ORIGIN` ต้อง quoteเพื่อให้ tokenถึง linker/loader
- missing library: เริ่มจาก `readelf -d`, SONAME/RUNPATH/search rules—not copy .soสุ่มเข้า system dirs

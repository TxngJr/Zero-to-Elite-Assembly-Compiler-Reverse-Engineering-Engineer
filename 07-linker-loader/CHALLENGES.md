# Challenges

- **07-A Mini Relocation Engine:** เพิ่ม signed PC32 range/overflow checksก่อน patch.
- **07-B Archive Order:** สร้าง 2 archivesที่อ้างกันและอธิบาย group optionsจาก evidence.
- **07-C Versioned Shared Demo:** SONAME `libcalc.so.1`, symlinks, app; แยก link-name/SONAME/real filename.
- **07-D Visibility Audit:** export public APIเพียง 2 symbolsแล้วตรวจ dynsym.
- **07-E Loader Mapping Report:** จับคู่ `readelf -l` กับ `/proc/$PID/maps` ของ course app.

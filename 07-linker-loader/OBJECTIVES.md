# Objectives

เมื่อจบบทนี้ควรสามารถ:
- อธิบาย symbol definition/reference และ resolution
- แยก local/global/weak conceptsใน linking context
- อธิบาย static archive extractionแบบ demand-driven
- อ่าน relocation recordsและคำนวณ toy `S+A` / `S+A-P`
- อธิบาย static vs dynamic linking
- อธิบาย PIC/PIE, GOT, PLT
- อ่าน `DT_NEEDED`, SONAME, RPATH/RUNPATH
- อธิบาย dynamic loader search/resolutionภาพใหญ่
- ใช้ `ar`, `nm`, `readelf -r/-d`, `objdump -dr`, `ldd`อย่างระมัดระวัง
- อธิบาย constructors/init arraysและ startup sequenceแบบย่อ
- สร้าง static/shared librariesและ executableที่ใช้ `$ORIGIN`
- เข้าใจ symbol interposition/visibilityระดับ concept

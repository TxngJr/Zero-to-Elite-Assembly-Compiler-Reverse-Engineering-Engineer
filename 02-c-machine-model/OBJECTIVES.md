# Objectives

เมื่อจบบทนี้ ผู้เรียนควรสามารถ:

- อธิบาย source → preprocess → assembly → object → executable
- แยก variable name, C object, type, value, address และ storage
- ใช้ fixed-width integer types และ `sizeof` อย่างถูกต้อง
- อธิบาย pointers, dereference, pointer arithmetic และ array decay
- อธิบายว่า array ไม่ใช่ pointer
- อ่าน string representation และออกแบบ bounded string operations
- ตรวจ struct padding/alignment ด้วย `offsetof`/`sizeof`
- อธิบาย stack/heap โดยไม่ยึด layout แบบตายตัว
- แยก scope, lifetime/storage duration และ linkage
- ใช้ function pointers, `const`, `volatile` อย่างไม่เข้าใจผิด
- ใช้ preprocessor/header/multi-file compilation
- แยก undefined/implementation-defined/unspecified behavior
- ใช้ compiler warnings, ASan/UBSan และ GDB เพื่อหาบัค
- เปรียบเทียบ `-O0` กับ optimized assembly โดยไม่คาดว่า source variable ต้องอยู่ใน memory
- สร้าง mini-string, dynamic-array, arena allocator และ hexdump utility

# Common Mistakes

- Variable = กล่องใน RAM เสมอ — optimizer อาจใช้ register/constant/remove
- Pointer = integer address ธรรมดา — มี type/semantic constraints
- Array = pointer — array อาจ decay แต่เป็นคนละ object/type concept
- `sizeof(pointer)` = target size — ผิด
- `sizeof(array parameter)` = caller array size — ผิด
- String ไม่มี terminator — valid C string ต้องมี `\0`
- `malloc` คืน zeroed memory — ผิด
- assign `realloc` กลับ pointer เดิมปลอดภัยเสมอ — ผิด
- Stack/heap address ตายตัว — ไม่ใช่ C guarantee
- `const` = compile-time/read-only memory เสมอ — ผิด
- `volatile` = thread-safe/atomic — ผิด
- Signed overflow wraps — UB
- Dump struct raw = portable format — ผิด
- Warnings/sanitizers prove correctness — ไม่ใช่ proof
- Source line = assembly instruction 1:1 — ผิด

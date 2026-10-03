# Labs

ทุก lab ใช้ **Predict → Run → Inspect → Explain → Modify**

## Lab 02-01 — Full C pipeline
ใช้ `object_model.c` สร้าง `.i`, `.s`, `.o`, executable; เทียบ types/sizes และหา symbol `main` ด้วย `nm`.

## Lab 02-02 — Type sizes
รัน `type_sizes.c`; ก่อนรันทำนาย `CHAR_BIT`, sizes ของ integer/pointer แล้วแยก C guarantees จาก Fedora/x86-64 observation.

## Lab 02-03 — Pointer anatomy
ใช้ `pointers.c`; วาด `x,p,&x,&p,*p` และทำนาย `*p=99`.

## Lab 02-04 — Array vs pointer
ใช้ `arrays.c`; ทำนาย `sizeof array`, `sizeof pointer`, `a+1`, `&a+1`.

## Lab 02-05 — String bytes
ใช้ `string_bytes.c`; ทำนาย bytes/terminator ของ "ABC", length vs storage และ embedded null.

## Lab 02-06 — Struct padding
ใช้ `struct_layout.c`; ทำนาย offsets แล้วสลับ member order. ห้ามสรุป layout เป็น universal rule.

## Lab 02-07 — Storage addresses
ใช้ `storage_regions.c` แสดง global/static/automatic/allocated addresses; รันหลายรอบและสังเกต ASLR. Ordering ไม่ใช่ C guarantee.

## Lab 02-08 — Function pointer
ใช้ `function_pointer.c`; เปลี่ยน callback และดู `gcc -S -O0` เพื่อหา call shape.

## Lab 02-09 — Preprocessor and multi-file
ใช้ `examples/multifile/`: preprocess, compile .o แยก, `nm` defined/undefined symbols แล้ว link.

## Lab 02-10 — UB with sanitizers
Build `buggy_bounds.c` ด้วย ASan/UBSan ใน local lab, อ่าน report, แก้ index แล้ว verify.

## Lab 02-11 — Optimization comparison
Compile `optimization.c` ที่ `-O0`/`-O2`; diff assembly แล้วอธิบายสิ่งที่ถูก fold/eliminate.

## Lab 02-12 — GDB memory inspection
Compile `gdb_target.c -O0 -g`; break `inspect_me`, ใช้ `print`, `x/16bx`, `backtrace`, `info registers`, `disassemble /m`.

## Lab 02-13 — Mini String
เพิ่ม tests capacity 0, exact fit, one-byte-too-small.

## Lab 02-14 — Dynamic Array
ทำนาย capacity growth, push 100 elements, invalid index, overflow guard.

## Lab 02-15 — Arena Allocator
ทำนาย offsets/alignment ของ allocations 1/4/7 bytes align 1/4/8 และ reset behavior.

## Lab 02-16 — Hexdump
dump text/executable ของเราเอง; อ่าน offsets, hex bytes, ASCII และหา ELF magic `7f 45 4c 46`.

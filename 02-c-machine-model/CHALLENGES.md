# Challenges

## Challenge 02-A — Safe record serializer
Serialize `{uint8_t type; uint32_t id; uint16_t flags;}` เป็น explicit little-endian bytes โดยไม่ dump raw struct. เขียน encode/decode + tests.

## Challenge 02-B — Pointer/array proof
แสดง `sizeof a`, `sizeof p`, addresses ของ `a,a+1,&a,&a+1` สำหรับ `int a[4]`; prediction เป็น offsets ไม่ใช่ exact address.

## Challenge 02-C — Robust vector growth
ขยาย dynamic-array ให้ตรวจ integer overflow ก่อน allocation bytes, preserve old allocation เมื่อ `realloc` fail และมี edge tests.

## Challenge 02-D — Arena typed helpers
เพิ่ม helper allocate N elements พร้อม overflow check `count*size` และ alignment; failure ต้องไม่ทำ state เสีย.

## Challenge 02-E — Hexdump compare
เทียบ utility กับ `xxd`/`hexdump -C` บน empty/text/executable ที่เราสร้างเอง; ยืนยัน bytes ตรงกัน.

## Challenge 02-F — Reverse the optimizer (intro)
เขียน arithmetic function, compile O0/O2, อธิบาย behavior จาก optimized assembly shape โดยไม่พึ่งจำ register names แล้วค่อยเปิด source ตรวจ.

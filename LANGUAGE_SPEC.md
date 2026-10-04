# EliteLang Language Specification — v0.2

EliteLang เป็นภาษา educational subset สำหรับ Chapters 09–12. เอกสารนี้เป็น **semantic contract** ระหว่าง frontend, IR optimizer และ x86-64 backend.

## 1. Program entry point

ทุกโปรแกรมต้องมี:

```text
fn main() -> int
```

เวอร์ชันนี้ไม่รองรับ parameters ของ `main`. การรับ command-line arguments ต้องมี runtime design แยกต่างหากในอนาคต.

## 2. Types

### `int`

- signed 64-bit two's-complement
- ช่วงค่าที่ represent ได้: `-2^63 ... 2^63-1`
- decimal integer literal โดยตรงรับ `0 ... 2^63-1`
- ค่า `-2^63` สร้างได้จาก expression เช่น `-9223372036854775807 - 1`

### `bool`

- source values: `true`, `false`
- backend normalizes boolean results เป็น 0 หรือ 1

## 3. Integer arithmetic

### `+`, `-`, `*`

ใช้ signed 64-bit two's-complement **wrapping** semantics. ผลลัพธ์เทียบเท่าการคำนวณ modulo `2^64` แล้วตีความกลับเป็น signed 64-bit.

### `/`, `%`

- signed division
- quotient truncates toward zero
- remainder: `a - trunc(a/b) * b`
- division by zero traps at runtime
- `INT64_MIN / -1` และ `INT64_MIN % -1` trap เพราะ x86-64 `idiv` overflow

Optimizer ต้อง preserve trap behavior: ถ้าการ fold constant จะลบ trap ดังกล่าว ต้องไม่ fold expression นั้น.

## 4. Comparisons

`< <= > >=` ใช้ signed integer comparison.

`== !=` ต้องเปรียบเทียบ operands ที่มี type เดียวกัน.

ผล comparison เป็น `bool`.

## 5. Logical operators

`&&` และ `||` ใช้ short-circuit evaluation.

ดังนั้น expression RHS ต้องไม่ execute เมื่อผลถูกกำหนดจาก LHS แล้ว.

## 6. Variables and scope

- `let name: type = expr;` สร้าง local binding
- assignment ไม่เปลี่ยน type
- nested block มี lexical scope
- educational version นี้ **ไม่อนุญาต shadowing** เพื่อให้ IR names อ่านง่าย

## 7. Functions

- parameters และ return type ต้องประกาศ
- recursion และ forward function references รองรับ
- argument count/type ต้องตรง signature
- current checker require explicit/obvious return path
- functions ที่อาศัย infinite loop เพื่อไม่ return ยังอาจถูก checker ปฏิเสธในเวอร์ชันนี้

## 8. Evaluation order

Arguments และ binary operandsถูก lower จากซ้ายไปขวาใน current implementation. โปรแกรมไม่ควรพึ่ง side effects ที่ language spec ยังไม่ได้ formalize เพิ่มเติม.

## 9. Runtime / ABI

Generated Linux x86-64 codeใช้ System V AMD64 ABI ภายใน compiled program และพึ่ง host compiler driver สำหรับ startup/linking.

EliteLang source ไม่ได้รับอนุญาตให้ประกาศ arbitrary external C functions ในเวอร์ชันนี้.

## 10. Known language limitations

ยังไม่มี:
- strings
- arrays
- pointers
- structs
- modules
- user-defined integer widths
- floating point
- heap/runtime standard library
- source-level DWARF
- exceptions

สิ่งเหล่านี้ต้องเพิ่มพร้อม grammar + type rules + IR semantics + backend + tests ไม่ใช่เพิ่มเฉพาะ parser.

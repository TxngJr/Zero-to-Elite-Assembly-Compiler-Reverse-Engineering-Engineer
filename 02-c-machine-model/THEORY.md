# Theory — C Machine Model

## 1. C pipeline revisited

ไฟล์ C ไม่ใช่ CPU instructions:

```text
program.c
   │ gcc -E
   ▼
program.i        preprocessed C
   │ compiler proper
   ▼
program.s        target assembly
   │ assembler
   ▼
program.o        relocatable object
   │ linker
   ▼
program          executable
```

ใช้ `gcc -v`, `-E`, `-S`, `-c` เพื่อเห็นแต่ละ stage. `gcc` command เป็น driver ที่ orchestrate หลาย tools ได้.

## 2. Variables are typed objects—not guaranteed memory boxes

แยก:
- **identifier/name** — token ใน source
- **object** — region of data storage ตาม C abstract machine
- **type** — กฎ representation/operations
- **value** — abstract value
- **address** — pointer to object เมื่อ applicable
- **storage** — implementation mechanism จริงอาจเป็น memory/register/optimized away

```c
int x = 42;
printf("%zu %p\n", sizeof x, (void *)&x);
```

การ take address ทำให้ address observable แต่ไม่แปลว่า source variable ทุกตัวต้องมี memory slot ในทุก build.

## 3. Integer types and portability

`char`, `short`, `int`, `long`, `long long` มี minimum requirements แต่ size จริงขึ้นกับ implementation. ใช้ `<limits.h>`, `<stdint.h>`, `<inttypes.h>`. Exact-width type เช่น `uint32_t` มีเมื่อ implementation รองรับ exact width นั้น.

## 4. `sizeof`

`sizeof` คืนจำนวน C bytes เป็น `size_t`. สำหรับ array:

```c
int a[10];
sizeof a
sizeof a[0]
sizeof a / sizeof a[0]
```

แต่ array parameter ถูก adjusted เป็น pointer; `sizeof` pointer ไม่บอกจำนวน elements.

## 5. Addresses

```c
int x = 10;
printf("%p\n", (void *)&x);
```

Address ใน Linux user process โดยทั่วไปเป็น virtual address. ASLR ทำให้ exact addresses เปลี่ยนได้; อย่าเขียน test ที่พึ่ง address ตายตัว.

## 6. Pointers

```c
int x = 10;
int *p = &x;
```

```text
x   : int object containing 10
&x  : pointer to x
p   : pointer object pointing to x
*p  : lvalue designating x through p
```

Pointer มี type และ semantic constraints มากกว่าการเป็น integer address.

## 7. Pointer arithmetic

ถ้า `p` ชี้ element ใน array, `p+1` ชี้ element ถัดไป—not next byte เว้นแต่ pointed type size=1 C byte. Defined arithmetic จำกัดอยู่ใน array object เดียวกันและ one-past. One-past pointer ใช้ comparison/arithmetic บางกรณีได้แต่ห้าม dereference.

## 8. Arrays are not pointers

Array เป็น object ของ elements ต่อเนื่อง. ในหลาย expressions array converts/decays เป็น pointer to first element แต่ไม่ decay ในบาง contexts เช่น `sizeof` และ unary `&`.

`a`, `&a[0]`, `&a` อาจเริ่มที่ numeric address เดียวกัน แต่ types/stride ต่างกัน.

## 9. Strings

C string คือ sequence ของ `char` ที่มี null terminator:

```text
"ABC" → 41 42 43 00
```

String literal ไม่ควรถูกแก้ไข. Bounded copy API ควรรู้ destination capacity เพื่อหลีกเลี่ยง out-of-bounds.

## 10. Structs, padding, alignment

Compiler อาจแทรก padding เพื่อ alignment:

```c
struct record { char tag; int value; short code; };
```

ตรวจด้วย `sizeof` และ `offsetof`. อย่า dump raw struct เป็น portable file/network format โดยไม่มี explicit ABI/format contract.

## 11. Unions

Union members share storage. ใช้สอน shared representation ได้ แต่ type-punning rules มีรายละเอียด; สำหรับ inspect object representation แบบ portable ใช้ `unsigned char *` หรือ `memcpy` เป็นหลัก.

## 12. Enums

Enum ให้ named integer constants และ enumerated type. Representation details ขึ้นกับ implementation/options; อย่าสมมติ fixed-width wire format.

## 13. Stack model—with caveats

Call stack เป็น model ที่ช่วยอธิบาย function calls/automatic objects แต่ exact layout ขึ้นกับ ABI/compiler/optimization. Optimizer อาจไม่มี traditional frame หรือไม่เก็บ local ใน stack. Lab ใช้ `-O0 -g` เพื่อสังเกตง่าย ไม่ใช่ C guarantee.

## 14. Heap/dynamic allocation

`malloc`, `calloc`, `realloc`, `free` จัดการ allocated storage. `malloc` ไม่ zero-initialize; `calloc` zero-initializes bytes. `realloc` อาจย้าย allocation.

Safe pattern:

```c
void *tmp = realloc(ptr, new_size);
if (tmp != NULL) ptr = tmp;
```

อย่า assign กลับ pointer เดิมก่อนตรวจ failure.

## 15. Storage duration vs scope

**scope** = source region ที่ name มองเห็น. **storage duration/lifetime** = object มี storage นานแค่ไหน. สำคัญ: automatic, static, allocated; thread storage duration มีใน C11 implementations ที่รองรับ.

## 16. Linkage: `static` and `extern`

File-scope `static` มักให้ internal linkage; `extern` declaration อ้าง entity ที่ definition อยู่ translation unit อื่นได้. Block-scope `static` เน้น static storage duration—not internal linkage ของ local name.

## 17. Functions

แยก declaration/prototype/definition. Function call ใน source ถูก map สู่ target calling convention/ABI ซึ่งจะเรียนลึกใน Chapter 04.

## 18. Function pointers

```c
int (*fn)(int,int) = add;
int result = fn(2,3);
```

ใช้ callbacks/dispatch. ที่ machine level เกี่ยวข้องกับ indirect control transfer.

## 19. `const`

```c
const int *p;
int *const p2 = ...;
const int *const p3 = ...;
```

`const` เป็น qualifier ที่จำกัด modification ผ่าน lvalue นั้น ไม่ได้แปลว่า compile-time constant/read-only memory เสมอ.

## 20. `volatile`

`volatile` ใช้กับ observable accesses บางบริบท เช่น memory-mapped I/O. มันไม่ทำให้ thread-safe, ไม่แทน atomics/mutex/memory ordering และไม่ใช่ “ปิด optimization ทั้งหมด”.

## 21. Bit-fields

Bit-fields สะดวกแต่ allocation/packing details หลายอย่าง implementation-dependent. Portable protocols มักใช้ explicit masks/shifts/byte serialization.

## 22. Preprocessor

`#include`, `#define`, `#ifdef`, header guards เป็น preprocessing. ดูผลด้วย `gcc -E`. Macro ไม่ typed และอาจ evaluate argument หลายครั้งถ้าออกแบบไม่ดี.

## 23. Translation units and multi-file builds

```text
main.c ───────→ main.o
math_utils.c ─→ math_utils.o
        \       /
          linker
            ↓
         program
```

Headers ให้ shared declarations; source files ให้ definitions; linker resolve external symbols.

## 24. Undefined / implementation-defined / unspecified

- **Undefined behavior:** standard ไม่กำหนด requirements เมื่อเกิด operation นั้น เช่น out-of-bounds, use-after-free, signed overflowบางกรณี
- **Implementation-defined:** implementation เลือก behavior และ document choice
- **Unspecified:** standard อนุญาตหลาย possibilities โดยไม่บังคับ document choice สำหรับ occurrence นั้น

## 25. Warnings and sanitizers

Baseline:
```bash
gcc -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g file.c
```

Sanitizers:
```bash
gcc -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer buggy.c
```

Warnings/sanitizers ช่วยพบปัญหาแต่ไม่พิสูจน์ correctness ทั้งหมด.

## 26. Optimization changes observability

เปรียบเทียบ `-O0` และ `-O2`. Compiler อาจ constant-fold, inline, eliminate dead code, keep values in registers, remove source variables. Reverse engineering ต้อง reconstruct semantics ไม่ใช่คาด one-line = one-instruction.

## 27. Basic assembly shapes from C

ตอนนี้ให้รู้จัก shape: data movement, arithmetic, compare, branch, call, return. ชื่อ x86 instructions/registers จริงเริ่ม Chapter 03.

## 28. GDB as microscope

ใช้ `break`, `run`, `next`, `step`, `print`, `x`, `info registers`, `backtrace`, `disassemble`. Debugger observation ของ UB ไม่ทำให้ UB กลายเป็น defined behavior.

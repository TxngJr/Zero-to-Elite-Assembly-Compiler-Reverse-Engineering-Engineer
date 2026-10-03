# Answers and Hints

## Pointer/array reference
```c
int a[4];
int *p = a;
```
`sizeof a` คือ whole array, `sizeof p` คือ pointer size; `a+1` เลื่อนหนึ่ง int, `&a+1` เลื่อนหนึ่ง whole array. Starting numeric address อาจเท่ากันแต่ types/stride ต่างกัน.

## `realloc` safe direction
```c
void *tmp = realloc(ptr, new_bytes);
if (tmp == NULL) return failure;
ptr = tmp;
```
ตรวจ overflow ของ multiplication ก่อน.

## Struct
ใช้ `offsetof`/`sizeof` เป็น evidence และอย่า serialize raw struct สำหรับ portable format.

## Sanitizer
อ่าน error class → failing source access → stack trace → allocation/free origin → root cause → fix → rerun.

## Optimizer
Constant-only expressions อาจถูก fold; dead work อาจถูกลบ ตราบใดที่ observable behavior ของ defined program ถูก preserve.

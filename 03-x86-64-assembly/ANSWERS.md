# Answers and Hints

- EAX write zeroes upper 32 bitsของ RAX; AX/ALไม่ทำ
- `[rax+rcx*8+16]` เมื่อ 0x1000,3 = 0x1028
- CMP set flags; jccเลือก signed/unsigned interpretation
- `lea rax,[rdi+rdi*2]` = 3×RDIโดยไม่ dereference
- SHR zero-fill; SAR sign-fill
- CALLเก็บ return address; argument passingเป็น ABI

Challenge hints: clamp compare boundsทีละด้าน; popcount add low bitแล้ว shift; reverse stopเมื่อ left>=right; int32 index scale=4.

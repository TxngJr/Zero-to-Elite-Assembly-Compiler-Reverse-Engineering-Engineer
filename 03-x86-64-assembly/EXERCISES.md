# Exercises

1. RAX/EAX/AX/ALสัมพันธ์กันอย่างไร
2. หลัง `mov rax,-1; mov eax,5` RAX?
3. หลัง `mov rax,-1; mov ax,5` upper bits?
4. immediate/register/memory operandอย่างละตัวอย่าง
5. `mov eax,[rbx]` อ่านกี่ bytes
6. `mov rax,[rbx]` อ่านกี่ bytes
7. movzx vs movsx
8. 0xFF ผ่าน zero/sign extensionเป็นอะไร
9. ADD/SUB set flagsอะไรที่เราใช้
10. `cmp` เก็บผลหรือไม่
11. `test eax,eax` ใช้เช็ค zeroอย่างไร
12. CFเหมาะกับ reasoningแบบใด
13. OFหมายถึงอะไร
14. jl vs jb
15. signed jcc 4 ตัว
16. unsigned jcc 4 ตัว
17. สร้าง CFG ของ if/else เล็ก ๆ
18. `[rax+rcx*8+16]` เมื่อ RAX=0x1000, RCX=3
19. addressing scaleที่รองรับ
20. int32 array scale
21. int64 array scale
22. RIP-relativeมีประโยชน์อะไร
23. LEA dereferenceหรือไม่
24. `lea rax,[rdi+rdi*2]` คำนวณอะไร
25. general memory-to-memory MOVทำได้หรือไม่
26. AND mask clear bitsอย่างไร
27. OR set bitsอย่างไร
28. XOR toggle bitsอย่างไร
29. SHR/SARต่างกัน
30. rotateต่างจาก shift
31. variable shift countใช้ registerส่วนใด
32. push qwordเปลี่ยน RSPอย่างไร
33. popเปลี่ยน RSPอย่างไร
34. callเก็บอะไร
35. retอ่านอะไร
36. call semanticsต่างจาก calling conventionอย่างไร
37. stack imbalanceก่อน retอันตรายอย่างไร
38. directive vs instruction
39. `.text/.data/.rodata/.bss`
40. `objdump -dr` เห็นอะไร
41. `readelf -s` เห็นอะไร
42. `si` vs `ni`
43. optimized outputทำไมไม่ map 1:1 source
44. `xor eax,eax` vs `mov eax,0` ต่างด้าน flagsอย่างไร
45. cmovอ่าน conditionจากไหน
46. setccเขียน outputขนาดใด
47. `idiv` ทำไมซับซ้อนกว่า add
48. upper-halfของ multiplicationสำคัญเมื่อใด
49. partial-register writesต้องระวังอะไรเชิง semantics
50. เขียน mental checklist 7 ข้อก่อน reverse assembly function

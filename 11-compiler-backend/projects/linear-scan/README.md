# Linear-Scan Allocation Lab

นี่คือ **register-allocation algorithm จริงในระดับ live intervals** ไม่ใช่แค่คำอธิบาย.

`linear_scan.py`:
- expire intervals ที่ตายก่อน current start
- reuse free registers
- เมื่อ register pressure สูงเกิน budget ให้ spill
- ใช้ heuristic spill interval ที่ end ไกลกว่า current

```bash
python3 linear_scan.py
python3 linear_scan.py --json
```

## สิ่งที่ lab นี้พิสูจน์

- live intervals ที่ไม่ overlap reuse register ได้
- intervals ที่ overlap ต้องใช้ location ต่างกัน
- finite registers ทำให้เกิด spills
- spill heuristic มีผลต่อ allocation result

## สิ่งที่ยัง **ไม่** integrate ใน baseline backend

Chapter 11 code generatorหลักยังเป็น spill-everything เพื่อให้ instruction selection/ABI อ่านง่าย. การนำ allocatorนี้เข้า backendจริงยังต้องเพิ่ม:
- interval constructionจาก machine/IR positions
- call-clobber constraints
- fixed/precolored registers
- `idiv` constraints
- callee-saved save/restore
- spill load/store insertion
- phi/parallel-copy handling

ดังนั้นอย่าเขียน portfolio ว่า EliteC “ใช้ linear-scan allocationแล้ว” จนกว่าจะ integrate และมี differential tests.

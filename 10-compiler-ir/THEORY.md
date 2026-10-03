# Theory — Intermediate Representation

## 1. ทำไมต้องมี IR

ถ้า frontendต่อ x86-64โดยตรง ทุก syntax featureต้องรู้ target details. IRสร้าง boundary:

```text
many source constructs → common IR → many target backends
```

## 2. Three-address style

Elite IR operationsตัวอย่าง:

```text
%t1 = const 6
%t2 = const 7
%t3 = bin + %t1 %t2
x = mov %t3
ret x
```

หนึ่ง instructionทำงานเรียบง่าย ทำ analysis/codegenง่ายกว่า AST nested expressions.

## 3. Virtual Values

`%tN` เป็น compiler temporaries ไม่ใช่ CPU registers. Source variablesยังเป็น mutable symbolic namesใน non-SSA IR รุ่นนี้.

## 4. Basic Blocks

Basic blockมี single entry และ controlไหลภายในจน terminator เช่น:
- `jump label`
- `cjump cond true false`
- `ret value`

## 5. CFG

Control-Flow Graph:
- nodes = basic blocks
- directed edges = possible control transfers

CFGเป็นฐานของ liveness, dominators, loop analysis และ optimizations.

## 6. Lowering If

```text
cond
cjump cond then else
then: ...
  jump merge
else: ...
  jump merge
merge:
```

## 7. Lowering While

```text
jump cond
cond:
  ...
  cjump c body exit
body:
  ...
  jump cond
exit:
```

## 8. Short-Circuit Semantics

`a && b` ห้าม evaluate bเมื่อ a=false. ดังนั้น loweringต้องใช้ CFG ไม่ใช่ arithmetic ANDแบบตรง ๆ.

`a || b` เช่นเดียวกัน: เมื่อ a=true ไม่ evaluate b.

## 9. Predecessors / Successors

Successorsอ่านจาก terminator. Predecessorsสร้างย้อน edges. Join blockคือ blockที่มีหลาย predecessors.

## 10. Dominators

Block A dominates B ถ้าทุก pathจาก entryไป Bต้องผ่าน A. Entry dominatesทุก reachable block.

Dominator informationใช้สร้าง SSA, loop reasoningและ optimizations.

## 11. Immediate Dominator / Dom Tree

Production compilersสร้าง dominator tree. Course toolแสดง dominator setsเพื่อให้ algorithmชัดก่อน.

## 12. Data-Flow Equations

Livenessแบบ backward:

```text
OUT[B] = union(IN[S]) for successors S
IN[B]  = USE[B] ∪ (OUT[B] - DEF[B])
```

iterateจนถึง fixed point.

## 13. Liveness

Value liveที่ pointหนึ่งถ้ามี future useก่อนถูก redefine. Backendใช้ livenessช่วย register allocation.

## 14. Constant Folding

```text
%a = const 6
%b = const 7
%c = bin * %a %b
```

สามารถกลายเป็น `%c = const 42` หาก operation semanticsปลอดภัยและรู้ constantsจริง.

## 15. Constant Propagation

`x = const 42; y = mov x` อาจ propagate 42. Course optimizerทำ local propagationภายใน block.

## 16. DCE

Dead-code eliminationลบ definitionที่ไม่มี useและไม่มี side effect. **Calls/stores/traps** ต้องระวัง; “resultไม่ถูกใช้” ไม่ได้แปลว่า instructionลบได้.

## 17. Common Subexpression Elimination

หาก expressionเดียวกันเกิดซ้ำและ operandsไม่เปลี่ยน compilerอาจ reuse result. ต้อง reasonเรื่อง memory/side effects/aliasing.

## 18. SSA

Static Single Assignmentกำหนดให้ SSA nameถูก defineครั้งเดียว:

```text
x1 = ...
x2 = ...
```

ช่วยให้ data-flow use-def chainsชัด.

## 19. Phi

เมื่อ control pathsหลายทางให้ค่าต่างกัน:

```text
then: x1 = 40
else: x2 = 2
merge: x3 = phi(x1, x2)
```

Phiไม่ใช่ runtime function call; เป็น IR merge semanticsที่ backendต้อง eliminateภายหลัง.

## 20. Phi Placement

Full SSAใช้ dominance frontiers. Course tool `--ssa` แสดง **phi candidatesแบบง่าย** ที่ join blockเมื่อ source variableถูก defineในหลาย predecessor; นี่เป็น teaching aid ไม่ใช่ Cytron algorithmครบ.

## 21. Renaming

หลัง phi placement SSA conversionต้อง rename variable definitions/usesตาม dominator tree. จะต่อใน full compiler chapter.

## 22. Loops and Phi

Loop headersมักต้อง phi:
```text
i0 = 0
loop:
  i1 = phi(i0, i2)
  ...
  i2 = i1 + 1
```

## 23. Types in IR

Course IRถือว่า frontendตรวจ typesแล้วจึงไม่ encode detailed IR typesทุก instruction. Production IRควรเก็บ typesชัดเจนเพื่อ verification/codegen.

## 24. IR Verification

Verifierควรตรวจ:
- unique block labels
- terminatorทุก reachable block
- branch targets exist
- operand definitions/types
- call signatures
- CFG consistency

## 25. Optimization Correctness

Optimizationต้อง preserve observable semantics. Short-circuit, division-by-zero traps, overflow model และ callsทำให้ transformationsบางอย่างไม่ปลอดภัย.

## 26. Target Independence

IRยังไม่เลือก RAX/RDIหรือ x86 opcodes. Chapter 11ทำ instruction selectionและ ABI lowering.

## 27. Analysis vs Transformation

Analysisคำนวณ facts เช่น live sets; transformationเปลี่ยน IR. แยกสองอย่างช่วย test correctness.

## 28. Fixed Point

CFG cyclesทำให้ data-flowต้อง iterateจน stateไม่เปลี่ยน. Orderอาจกระทบ speedแต่ solutionต้องตรง lattice/framework assumptions.

## 29. Optimization Pipeline

ตัวอย่าง:
```text
lower → simplify CFG → constants → DCE → SSA → global opts → lower SSA
```

Order mattersเพราะ passหนึ่งเปิดโอกาสให้ passถัดไป.

## 30. IR Mental Checklist

blocks? terminators? edges? defs/uses? side effects? types? constants? liveness? dominance? join points? semantics preserved?

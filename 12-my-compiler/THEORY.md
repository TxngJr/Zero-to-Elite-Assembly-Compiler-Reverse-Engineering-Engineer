# Theory — Building a Complete Educational Compiler

## 1. Compiler Driver

Compiler driverคือ commandที่ orchestrate phases:

```text
read source
→ frontend
→ IR
→ passes
→ backend
→ write assembly
→ invoke assembler/linker
```

GCC/Clangเองก็ทำหน้าที่ driverคล้ายแนวคิดนี้.

## 2. Stable Phase Boundaries

แต่ละ phaseควรรับ/คืน representationชัด:

- lexer: text → tokens
- parser: tokens → AST
- checker: AST → validated AST/metadata
- lowerer: AST → IR
- optimizer: IR → IR
- backend: IR → assembly

การรักษา boundaryช่วย testแต่ละ stageแยกกัน.

## 3. CLI as an Engineering Interface

EliteC รองรับ:

```text
--check
--emit tokens
--emit ast
--emit ir
--emit asm
--opt
-o OUTPUT
--run
--cc DRIVER
```

Intermediate-output modesสำคัญต่อ debugging compiler.

## 4. Compiler Errors vs Program Errors

แยก:

- compiler diagnostic: sourceไม่ valid / toolchain fail
- generated program exit code: semanticsของ programหลัง compileสำเร็จ

อย่าใช้ค่า return 42ของ programไปตีความว่า compilerล้มเหลว.

## 5. External Toolchain

EliteC emit GNU assemblyแล้วเรียก GCC/Clang driverเพื่อ assemble/link. ข้อดี:

- reuse mature assembler/linker
- ได้ ELF startup/runtimeตาม platform
- inspectง่าย

Direct ELF/object emissionเป็นขั้นต่อยอด ไม่ใช่ requirementของ educational compilerนี้.

## 6. Temporary Files

Driverใช้ temporary directoryสำหรับ assemblyเมื่อ compileปกติ เพื่อไม่ทิ้ง build noise. `--emit asm` ใช้เมื่อต้องการ inspect artifact.

## 7. Diagnostics

Frontend `CompileError` ต้องเดินขึ้นมาถึง driverโดยไม่กลายเป็น Python tracebackสำหรับ user errors. Internal compiler bugควรแยกจาก source diagnostic.

## 8. Optimization Flag

`--opt` เปิด local IR optimizationจาก Chapter 10. Compilerต้องมี testsพิสูจน์ optimized/unoptimized outputsให้ behaviorเดียวกันใน supported semantics.

## 9. End-to-End Testing

Minimum matrix:

- constant return
- arithmetic
- branch
- loop
- recursive call
- 0–8+ args
- signed division/modulo
- short-circuit
- type error
- syntax error

## 10. Differential Testing

สร้าง reference interpreterสำหรับ IR/ASTแล้ว compareกับ compiled executableเป็นวิธี powerfulในการหา backend bugs.

## 11. Golden Tests

AST/IR/assembly outputสามารถใช้ golden snapshotได้ แต่ brittleเมื่อ formattingเปลี่ยน. Behavioral testsควรเป็นแกนหลัก.

## 12. Determinism

Compiler inputเดียว + version/optionsเดียวควร emit output deterministicเท่าที่ practical. Random temp pathsไม่ควร leakเข้า semantic artifactsโดยไม่จำเป็น.

## 13. Language Versioning

เมื่อ grammar/semanticsเปลี่ยน ควรมี version strategyก่อน ecosystemใหญ่ขึ้น. Course compilerยังไม่ freeze language spec.

## 14. Integer Model

EliteLang backendใช้ signed 64-bit integer machine model. Literal overflow policyยังเป็น challengeจาก Chapter 09.

## 15. Boolean Model

`false=0`, `true=1`; comparisons normalizeเป็น 0/1. Short-circuit semanticsถูก encodeใน CFG.

## 16. Runtime

ตอนนี้ compilerพึ่ง C runtime startup/linkingจาก compiler driver แต่ languageไม่มี standard libraryของตัวเอง. Chapterนี้แยก “compiler” ออกจาก “language runtime”.

## 17. Object Files

Production compilerอาจ emit `.o` แล้ว linkภายหลัง. Course driverข้ามตรงไป assembly→executableเพื่อเห็น pipelineชัด.

## 18. Debug Information

Generated assemblyไม่มี source-level DWARF mappingของ EliteLang. GDBจึงเห็น function/assemblyแต่ไม่ mapกลับ EliteLang sourceอย่างสมบูรณ์.

## 19. Register Allocation Gap

Chapter 11อธิบาย linear scan/graph coloring แต่ implementation baselineยัง spillทุก value. Chapter 12ถือสิ่งนี้เป็น conscious design debt—not hidden bug.

## 20. SSA Gap

Chapter 10มี SSA concepts/phi candidates แต่ full SSA constructionยังไม่ integrate. Compilerยัง correctได้โดยใช้ mutable stack slots.

## 21. Optimization Correctness

Passต้อง preserve:
- short-circuit
- call side effects
- division traps
- signed semantics
- control flow

Optimization bugเป็น compiler correctness bug.

## 22. Compiler Self-Hosting

Self-hostingหมายถึง compilerถูกเขียนด้วยภาษาที่ตัวเอง compileได้. EliteLangยังเล็กเกินไปและ compilerเขียน Python จึงไม่ self-hosting.

## 23. Bootstrapping

Compiler bootstrapอาจเริ่มจาก implementationใน host language แล้วเพิ่ม languageจนเขียน compilerตัวเองได้. Self-hostingไม่จำเป็นต่อความเป็น compilerจริง.

## 24. Cross Compilation

Hostกับ targetต่างกันได้. ตอนนี้ host/targetคือ Linux x86-64; OS chaptersจะช่วยให้เข้าใจว่าการ target bare-metalต้องเปลี่ยน runtime/ABI assumptions.

## 25. Frontend Extensibility

Featureใหม่ควรคิดครบ:
grammar → AST → type rules → lowering → IR semantics → backend → tests.

## 26. Pass Manager Concept

เมื่อ passesเพิ่ม ควรมี ordered pipelineและ verificationระหว่าง passes. Courseยังเรียก optimizerตรง ๆ เพราะมี passน้อย.

## 27. Internal Verification

Debug buildsของ compilerควร assert invariants เช่น block terminators/known targets/use definitions. Verifierช่วยจับ compiler bugใกล้จุดสร้าง.

## 28. Fuzzing Compiler Inputs

Parser/compilerเป็นโปรแกรมที่อ่าน untrusted-ish textได้. Defensive parserควร reject malformed sourceโดยไม่ crash interpreterด้วย unexpected exceptions.

## 29. Reproducible Bug Report

Compiler bug reportควรมี:
- minimal source
- exact CLI/options
- compiler commit/version
- expected behavior
- actual diagnostic/output
- emitted IR/assemblyถ้า relevant

## 30. From Compiler to OS

OS kernelไม่ได้มี libc/startupเหมือน normal process. Chapter 13–14จะเปลี่ยน mindsetจาก hosted environmentไป freestanding/bare-metal environment.

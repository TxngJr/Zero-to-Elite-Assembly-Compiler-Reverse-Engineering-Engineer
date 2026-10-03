# Labs

1. Run `--check` บน valid/invalid source.
2. Compare `--emit tokens` กับ Chapter 09 output.
3. Inspect ASTของ factorial.
4. Inspect IR/CFGของ loop.
5. Compare optimized vs unoptimized IR.
6. Emit assemblyและ annotate function prologue/calls.
7. Compile factorialเป็น ELFและ inspectด้วย `file/readelf/objdump`.
8. Compileด้วย GCCและ Clang driver; compare behavior.
9. Test recursive factorial.
10. Test 8-argument call.
11. Test short-circuitที่ RHSหารศูนย์แต่ไม่ execute.
12. Trigger syntax/type diagnosticและยืนยันไม่มี Python traceback.
13. Use `--run` แล้วแยก compiler statusจาก program status.
14. Create minimal compiler bug reportจาก intentionally modified local copy.
15. Add one end-to-end regression case.

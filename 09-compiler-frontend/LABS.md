# Labs

1. Tokenize `valid.el`; classify keyword/identifier/operator.
2. เพิ่ม comments/whitespaceโดย ASTต้องไม่เปลี่ยน semantics.
3. วาด AST ของ `1 + 2 * 3` ก่อนเปิด `--ast`.
4. เปลี่ยน precedence parserชั่วคราวและสังเกต ASTผิด.
5. Trigger missing `;`, `}`, invalid character.
6. Trigger unknown variable.
7. Trigger wrong function arity.
8. Trigger int/bool mismatch.
9. Trace signature-table buildก่อน checking bodies.
10. Trace nested if/while scopes.
11. เพิ่ม unary expression test.
12. เพิ่ม call returning boolใน condition.
13. ทดสอบ duplicate function/parameter.
14. เพิ่ม source line/column diagnosticเป็น extension.
15. สร้าง grammar cheat sheetจาก parser code.

# Exercises — Compiler Frontend

## Response contract

ทุกข้อให้ตอบ 4 ส่วน:
1. **Explain** — อธิบายด้วยภาษาตัวเอง
2. **Concrete example** — ใช้ source/AST/tokenจริง
3. **Evidence** — command, AST fragment, diagnostic หรือ test
4. **Boundary / misconception** — สิ่งที่มักเข้าใจผิดอย่างน้อยหนึ่งข้อ

## A. Lexer / Tokens

1. สร้าง source 5 บรรทัดที่มี keyword, identifier, integer, comment และ multi-character operator; เขียน token streamด้วยมือก่อนรัน `--tokens`.
2. อธิบาย token vs lexemeโดยยก `IDENT foo` และ `INT 42` เป็นตัวอย่าง.
3. แก้ local lexerชั่วคราวให้ตรวจ identifierก่อน keywordแล้วทำนาย bug; คืน codeหลังทดลอง.
4. สร้าง inputที่มี characterไม่รองรับและตรวจว่า diagnosticระบุตำแหน่งโดยไม่ traceback.
5. อธิบาย maximal-munchด้วย `<=` เทียบ `<` + `=`.
6. สร้าง commentติดท้าย statementและพิสูจน์ว่ามันไม่สร้าง AST node.
7. อธิบาย EOF tokenมีประโยชน์ต่อ parser loop/errorอย่างไร.

## B. Parser / Precedence

8. วาด AST ของ `1 + 2 * 3 == 7 && true`; ยืนยันด้วย `--ast`.
9. วาด AST ของ `(1 + 2) * 3`; ระบุ nodeที่เปลี่ยนจากข้อ 8.
10. อธิบาย associativityของ `10 - 3 - 2` และพิสูจน์ tree.
11. สร้าง sourceที่ขาด `;`, `)`, และ `}` อย่างละหนึ่ง; เก็บ diagnostics.
12. อธิบายว่าทำไม recursive-descent grammarต้องหลีก left recursion.
13. เพิ่ม local syntax featureเล็ก ๆ ใน branch/working copy เช่น unary `+` พร้อม parser tests; อธิบายทุก phaseที่ต้องแตะ.
14. สร้าง call expression nested `f(g(1), h(2+3))` และวาด tree.

## C. Semantic / Type Checking

15. สร้าง program syntax-validแต่ `let x: bool = 42`; อธิบายว่าทำไม parserผ่านแต่ checkerไม่ผ่าน.
16. ทดสอบ unknown variable, unknown function, wrong arity, wrong argument type อย่างละหนึ่ง.
17. พิสูจน์ forward function referenceและ recursionว่า signaturesต้อง collectก่อน check bodies.
18. สร้าง duplicate functionและ duplicate parameter; อธิบาย scopeของแต่ละ error.
19. ทดสอบ `if (1)` และ `while (1)`; อธิบาย type rule.
20. ทดสอบ equality `1 == true`; อธิบายว่าทำไม operandsต้อง typeเดียวกัน.
21. สร้าง `main(x:int)` และ `main()->bool`; เก็บ evidenceว่า entry signatureถูกบังคับ.
22. ทดสอบ literal `9223372036854775807` และ `9223372036854775808`; เชื่อมกับ `LANGUAGE_SPEC.md`.

## D. Scope / Control Flow

23. สร้าง nested blockที่ประกาศชื่อซ้ำและยืนยัน current no-shadowing policy.
24. อธิบาย scope vs lifetimeโดยเทียบ checker environmentกับ runtime stack frame.
25. เขียน functionที่ returnในทั้งสอง branchและ functionที่ขาด returnหนึ่ง path; เปรียบเทียบ checker.
26. อธิบาย limitationของ current “obvious return” analysisด้วย infinite loopหรือ more complex control flow.

## E. Diagnostics / Engineering

27. เพิ่ม negative unit testหนึ่งตัวก่อนแก้ bugใด ๆ แล้วแสดง red→green evidence.
28. เปลี่ยน diagnosticหนึ่งจุดให้มี contextดีขึ้นโดยไม่ทำ testsเดิมพัง.
29. สร้าง malformed input 20 แบบด้วย scriptเล็ก ๆ และยืนยัน frontendไม่ crashด้วย unexpected Python exception.
30. เขียน frontend→IR contract 10 ข้อ: AST invariantsอะไรที่ lowererสามารถเชื่อถือได้.

## Practical submission

ส่ง:
- token prediction 2 ชุด
- AST drawings 3 ชุด
- negative diagnosticsอย่างน้อย 8 cases
- code/test patch 1 ชิ้น
- reflectionว่าความผิดพลาดแรกของคุณอยู่ lexer/parser/checker phaseใดและหาได้อย่างไร

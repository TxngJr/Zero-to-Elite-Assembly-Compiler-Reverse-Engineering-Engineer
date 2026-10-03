# Common Mistakes

- lexerทำ parsing logicมากเกินไป
- parserทำ type checkingปนจนแก้ยาก
- precedenceผิดแต่ sampleง่ายยังผ่าน
- ASTเก็บ punctuationทุกตัวโดยไม่จำเป็น
- symbol tableเดียวสำหรับทุก scopeแบบไม่มี model
- unknown identifierถูกปล่อยถึง backend
- type checkerเดาจาก runtime
- diagnosticsไม่มี source location
- assume parser accepted = program semantically valid

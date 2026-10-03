# Challenges

- **09-A Source spans:** เปลี่ยน tokens/ASTให้เก็บ start/end และ diagnostic line:column.
- **09-B Else-if:** เพิ่ม grammarโดยไม่สร้าง ambiguity.
- **09-C Local scopes:** อนุญาต shadowingถูกต้องด้วย scope stackและ unique symbol IDs.
- **09-D Integer range policy:** define int64 literal rangeและ error overflow.
- **09-E Frontend fuzz corpus:** สร้าง deterministic valid/invalid corpusและ assertว่า parserไม่ crashนอก CompileError.

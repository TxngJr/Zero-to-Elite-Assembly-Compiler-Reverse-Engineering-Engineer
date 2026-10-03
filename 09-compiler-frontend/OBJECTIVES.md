# Objectives

เมื่อจบบทนี้ควรสามารถ:
- อธิบาย lexer/tokenizer, parser, AST, semantic analysis และ type checking
- ออกแบบ grammar พร้อม precedence/associativity
- เขียน recursive-descent parser
- แยก syntax error จาก semantic/type error
- สร้าง symbol/signature environment
- ตรวจ unknown identifiers, duplicate definitions และ function arity/types
- ตรวจ return type และ boolean conditions
- อธิบาย scope/lifetimeว่าเป็นคนละเรื่อง
- serialize ASTเพื่อ inspect/debug compiler
- ออกแบบ diagnosticsที่มีตำแหน่ง source
- เขียน tests ทั้ง valid/invalid programs

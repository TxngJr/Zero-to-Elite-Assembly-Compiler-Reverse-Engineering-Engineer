# Theory — Compiler Frontend

## 1. Frontend Pipeline

```text
characters → lexer → tokens → parser → AST → semantic/type checker
```

Frontendยังไม่สร้าง machine code. เป้าหมายคือเปลี่ยน textให้เป็น representationที่มีโครงสร้างและถูกต้องตามกฎภาษา.

## 2. Tokens

Lexerรวม charactersเป็น categories เช่น:
- keyword: `fn`, `let`, `if`
- identifier
- integer literal
- operators
- punctuation
- EOF

Whitespace/commentsอาจถูก discard แต่ source positionsควรเก็บเพื่อ diagnostics.

## 3. Maximal Munch

เมื่อ operators overlap เช่น `=` กับ `==`, lexerควรเลือก tokenที่ยาวเหมาะสมก่อน. EliteLang regexจึงวาง multi-character operatorsก่อน single-character tokens.

## 4. Grammar

Simplified:

```text
function  := "fn" IDENT "(" params? ")" "->" type block
block     := "{" statement* "}"
statement := let | assign | return | if | while | expr ";"
expr      := precedence-based expression
```

Grammarคือ language contract ไม่ใช่ parser implementation.

## 5. Recursive Descent

แต่ละ nonterminalมี function เช่น `parse_expr`, `parse_add`, `parse_primary`. อ่านง่ายและเหมาะกับ hand-written educational compiler.

## 6. Precedence

จากต่ำไปสูงใน EliteLang:
```text
||
&&
== !=
< <= > >=
+ -
* / %
unary ! -
primary
```

ดังนั้น `1 + 2 * 3` parseเป็น `1 + (2*3)`.

## 7. Associativity

Loopsใน parserทำ binary operatorsหลายระดับเป็น left-associative เช่น `10-3-2` → `(10-3)-2`.

## 8. AST

ASTตัด punctuationที่ไม่จำเป็นและเก็บ semantics:
- Function
- Block
- Let / Assign / Return / If / While
- Binary / Unary / Call / Var / Literals

ASTต่างจาก parse treeที่อาจเก็บ grammar nodesทุกชั้น.

## 9. Semantic Analysis

Parserยอมรับ `x + y`เชิง syntaxได้ แต่ checkerต้องรู้ว่า identifiersมีอยู่และ typesรองรับ `+`.

## 10. Symbol Environments

Environment map:
```text
name → type
```
Function signature table:
```text
function → ([param types], return type)
```

## 11. Type Rules

EliteLang:
- arithmetic: int × int → int
- relational int comparisons → bool
- equalityต้อง same type → bool
- `&&/||`: bool × bool → bool
- unary `-`: int → int
- unary `!`: bool → bool

## 12. Calls

Checkerตรวจ:
1. function exists
2. argument count
3. argument types
4. resulting return type

## 13. Scope

Course frontend copy environmentเมื่อเข้า nested block. เพื่อให้ backendง่าย รุ่นนี้ deliberately **ไม่อนุญาต shadowing** ของ active variable names.

## 14. Return Analysis

Frontendทำ conservative structural checkว่า functionมี returnบน obvious paths; `if/else`จะ guarantee returnเมื่อทั้งสองแขน guarantee. นี่ไม่ใช่ full control-flow proofของ language compilerระดับ production.

## 15. Error Recovery

Production parserมัก recoverเพื่อรายงานหลาย errors. Course parserหยุดที่ first errorเพื่อให้ control flowของ implementationชัดก่อน.

## 16. Diagnostics

Diagnosticที่ดีควรบอก:
- error class
- source position/span
- expected vs actual
- relevant name/type

EliteLangเก็บ byte positionใน tokens; line/column mappingเป็น challenge.

## 17. AST Serialization

`--ast` ใช้ JSON-like dataclass serializationเพื่อ inspect parser result. นี่เป็น debugging interface ไม่ใช่ stable external format.

## 18. Testing Frontends

ต้องมี:
- happy-path syntax
- precedence
- nested control flow
- comments/whitespace
- unknown variables/functions
- duplicate params/functions
- type mismatch
- wrong arity
- missing return
- malformed tokens/braces

## 19. Language Design Trade-offs

ทุก featureเพิ่ม parser/type/backend complexity. Course languageตั้งใจเล็กเพื่อให้เห็น compiler mechanics ไม่ใช่แข่งกับ C/Rust.

## 20. Frontend Contract

Frontend outputต้องมี semanticsชัดพอให้ IR layerไม่ต้อง parse textซ้ำ. Chapter 10จะ lower ASTเป็น basic blocks/three-address IR.

# Objectives

เมื่อจบบทนี้ควรสามารถ:
- อธิบายเหตุผลที่ compilerใช้ IR
- lower expressions/statementsเป็น three-address operations
- สร้าง basic blocks และ terminators
- สร้าง CFG predecessor/successor relations
- อธิบาย dominators
- ทำ liveness data-flow analysis
- อธิบาย use/def, live-in/live-out
- ทำ local constant propagation/folding
- อธิบาย dead-code eliminationและข้อจำกัด side effects
- อธิบาย SSA single-definition property
- ระบุ join pointsที่อาจต้องใช้ phi
- lower short-circuit booleanเป็น control flow
- แยก frontend semanticsจาก target machine details

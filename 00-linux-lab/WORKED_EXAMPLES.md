# Worked Examples — Linux Systems Laboratory

ใช้ตัวอย่างเหล่านี้แบบ **Predict → Run → Observe → Explain → Modify**. Output ที่เป็น address/PID/version อาจต่างได้; ให้เทียบ key evidence ไม่ใช่เลข exact.

## Example 1 — Shell vs process

**Goal:** Shell vs process

**Prediction:** ทำนายว่า $$ ตรงกับ PID ใด แล้วตรวจด้วย ps

**Command / action:**

```text
echo "$$"; ps -p $$ -o pid,ppid,comm,args
```

**Expected key evidence:** PID ใน echo และแถว ps ต้องตรงกัน; PPID/args อาจต่างตาม terminal.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** เปิด subshell ด้วย bash แล้วทำซ้ำเพื่อเห็น PID ใหม่.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 2 — Redirection ordering

**Goal:** Redirection ordering

**Prediction:** แยก stdout/stderr และพิสูจน์ว่าลำดับ 2>&1 สำคัญ

**Command / action:**

```text
./build/streams >out.txt 2>err.txt
```

**Expected key evidence:** out.txt มี stdout และ err.txt มี stderr.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** สลับเป็น 2>&1 >out.txt แล้วอธิบายว่าทำไมผลต่าง.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.

## Example 3 — C build pipeline

**Goal:** C build pipeline

**Prediction:** เห็น source เปลี่ยน representation ทีละ stage

**Command / action:**

```text
gcc -E examples/hello.c -o build/hello.i; gcc -S -O0 examples/hello.c -o build/hello.s; gcc -c examples/hello.c -o build/hello.o; gcc build/hello.o -o build/hello
```

**Expected key evidence:** hello.i/.s เป็น text; .o/executable เป็น ELF คนละชนิด.

**What may vary:** addresses, tool version, symbol addresses, formatting หรือ environment-specific metadata ที่ไม่ใช่ semantic invariant.

**Explain:** เขียนเหตุผลเชื่อม observation กลับไปยัง contract/mental model ใน Theory.

**Modification:** ใช้ file/readelf/nm ตรวจแต่ละ artifact.

**Reflection:** ถ้าผลไม่ตรง prediction ให้บันทึกว่า prediction ผิดเพราะ concept ไหน—not แค่แก้จน output ตรง.


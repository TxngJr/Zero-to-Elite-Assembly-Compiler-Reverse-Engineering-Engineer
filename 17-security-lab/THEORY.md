# Theory — Defensive Vulnerability Research

## 1. Security Research Workflow

Course workflow:

```text
scope
→ reproduce
→ minimize
→ observe
→ root cause
→ patch
→ regression
→ broader audit
→ report
```

อย่าข้ามจาก crashไป “impactสูง” โดยไม่มี evidence.

## 2. Scope and Authorization

ในบทนี้ targetคือ course codeเท่านั้น. ในงานจริงต้องมี written/clear authorizationและ rules of engagementก่อน testing.

## 3. Crash Is Not Automatically a Vulnerability

Crashอาจมาจาก:
- programmer invariant
- malformed local test
- resource exhaustion
- memory-safety defect

Security impactต้องพิจารณา trust boundary, controllability, privileges, reachabilityและ deployment context.

## 4. Root Cause vs Crash Site

Out-of-bounds writeอาจ crashภายหลังใน allocator/return path. Sanitizerช่วยจับ first invalid memory operationใกล้ root causeมากขึ้น.

## 5. Buffer Boundaries

ก่อน copy:

```text
claimed_length
actual_input_length
destination_capacity
terminator requirements
```

ต้องสัมพันธ์กันอย่างถูกต้อง.

## 6. Length-Prefixed Input

ถ้า byteแรกบอก payload length:
1. inputต้องมี header
2. claimed lengthต้องไม่เกิน bytesที่เหลือ
3. claimed lengthต้องไม่เกิน destination/API maximum
4. arithmetic `header + length` ต้องไม่ overflow

Parser labใช้ patternนี้.

## 7. Out-of-Bounds Read/Write

OOB accessคือ read/writeนอก object bounds. Consequencesตั้งแต่ wrong result/crashถึง security issueขึ้นกับ context.

Defensive fixคือ enforce object/input bounds—notหวังว่า adjacent memory “น่าจะว่าง”.

## 8. Use-After-Free

Pointerยังถูกใช้หลัง object lifetimeจบ. Fixต้องจัด ownership/lifetime model ไม่ใช่เพียง set pointerหนึ่งตัวเป็น NULLถ้ามี aliasesอื่น.

## 9. Double Free

free resourceซ้ำอาจ corrupt allocator/lifetime state. Ownership conventionsและ idempotent cleanup patternsช่วยลด risk.

## 10. Integer Overflow

Unsigned arithmetic wrapถูก defineแต่ยังสร้าง logic bugsได้. Signed overflowใน Cเป็น undefined behavior.

Size calculation:
```c
if (count > SIZE_MAX / elem_size) error;
bytes = count * elem_size;
```

## 11. Truncation

แปลง `size_t`ไป `uint16_t/int` อาจตัดค่าก่อน check. Validateก่อน narrow conversion.

## 12. Format Strings

หาก untrusted stringถูกใช้เป็น format argumentโดยตรง APIอาจตีความ specifiers. Defensive pattern:

```c
printf("%s", user_text);
```

แทน treat inputเป็น format.

## 13. Null / Invalid Pointers

Null checkไม่พอสำหรับ arbitrary pointers. API designควรชัด ownership, length, optionality.

## 14. Race Conditions

Check-then-actบน shared stateอาจ invalidทันทีหลัง check. Correct fixต้องใช้ synchronization/atomic transactionตาม invariant.

## 15. Sanitizers

ASan detectsหลาย memory errors.  
UBSan detects undefined operationsหลายชนิด.

Build example:

```bash
-fsanitize=address,undefined -fno-omit-frame-pointer -g
```

Sanitizersเป็น testing instrumentation ไม่ใช่ proof/security boundary.

## 16. Reading ASan Output

Focus:
1. error class
2. operation read/write + size
3. first frameใน project code
4. object allocation/lifetime context
5. shadow-memory details only as needed

## 17. UBSan

UBSan reportsเช่น:
- signed overflow
- bad shifts
- alignment issues
- invalid enum/boundsบางกรณี

Recovery modeอาจ continue; `-fno-sanitize-recover`ช่วย make tests failเร็ว.

## 18. Fuzzing

Fuzzer feeds many inputsเพื่อ discover crashes/invariants. Good target:
- deterministic
- no network
- fast
- no global state leaks
- parser API accepts byte buffer + length

## 19. Corpus

Seed corpusควร cover valid minimal/typical/edge cases. Random mutation aloneอาจใช้เวลานานเข้าถึง structured states.

## 20. Deterministic Fuzz Smoke Test

Course fuzz-labใช้ fixed PRNG seedและ bounded iterationsเพื่อ CI reproducibility. มันไม่แทน libFuzzer/AFL++ coverage-guided fuzzing.

## 21. Minimize

เมื่อเจอ crash ลด inputจนเหลือ bytesขั้นต่ำที่ยัง reproduce. Inputเล็กช่วย root-causeและ regression.

## 22. Regression Test

Testที่ดี:
- captures bug condition
- failsก่อน fix
- passesหลัง fix
- asserts intended behavior
- ไม่ rely on undefined behavior

## 23. Patch Analysis

Compare vulnerable/fixed:
- checkเพิ่มตรงไหน
- validationก่อน memory accessหรือหลัง?
- integer typesถูกไหม
- error pathคืน stateสะอาดไหม
- tests cover boundaryทั้ง sidesไหม

## 24. Hardening

Defense-in-depth:
- ASLR/PIE
- NX
- RELRO
- stack protector
- CFIบาง ecosystems
- sandboxing

Hardeningไม่ replace source-level bounds/lifetime fix.

## 25. Stack Protector

Canaryอาจ detect stack overwriteก่อน return แต่ไม่ได้ prevent all OOB writesหรือบอก root causeดีที่สุดเท่า sanitizer.

## 26. NX

Non-executable data pagesลด attack surfaceบางแบบ แต่ memory corruptionยังเป็น bug.

## 27. ASLR

Randomized addressesเพิ่ม uncertaintyต่อ address-dependent attacksแต่ไม่แก้ logic/memory defect.

## 28. RELRO

Makes relocation-related regions read-onlyตาม modeหลัง loader setup. เป็น linker/loader hardening layer.

## 29. Safe Parser API

```c
int parse(const uint8_t *data, size_t size, Output *out);
```

explicit sizeช่วย reasoningกว่า NUL assumptionsสำหรับ binary inputs.

## 30. Fail Closed

Malformed inputควรถูก rejectโดยไม่ partial mutationที่ callerเข้าใจว่า valid. Initialize outputหรือ commit stateหลัง validationครบ.

## 31. Resource Limits

Even memory-safe parserอาจ allocate huge memory/loopนาน. Validate complexity/size limitsตาม threat model.

## 32. Error Messages

Diagnosticsช่วย debugแต่ production serviceต้องระวัง leakageของ sensitive internal data. Course local toolsไม่มี secrets.

## 33. Crash Triage Automation

Scriptสามารถ extract:
- sanitizer class
- signal
- project frames
- input name/hash

Automationช่วย groupingแต่ humanยังต้อง verify root cause.

## 34. Severity

Severityขึ้นกับ:
- attacker control
- remote/local reachability
- privileges
- confidentiality/integrity/availability impact
- mitigations
- exploitability evidence

บทนี้ไม่ assign dramatic severityจาก bug classอย่างเดียว.

## 35. Disclosure

ใน third-party researchให้ตาม vendor/security policy, minimize sensitive detailsจน fixพร้อม และไม่ publish weaponized materialที่เพิ่ม harm.

## 36. Memory-Safe Languages

Rust/managed languagesลด bug classesจำนวนมากแต่ unsafe FFI, logic bugs, races, parser complexityยังต้อง audit.

## 37. Defensive C

Use:
- explicit lengths
- checked arithmetic
- ownership rules
- initialization
- compiler warnings
- sanitizers
- fuzzing
- code review

## 38. Reproduction Record

Keep:
- exact build
- sanitizer flags
- input file/hash
- command
- output
- commit
- environment

## 39. Security Report Structure

- scope
- summary
- reproduction in local lab
- technical root cause
- impact under stated assumptions
- fix
- regression/fuzz evidence
- residual risks

## 40. Mental Checklist

authorized? reproducible? minimal? root cause? bounds/lifetime/arithmetic? sanitizer evidence? fixed? regression? fuzzed? impact grounded? report clear?

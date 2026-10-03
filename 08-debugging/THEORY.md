# Theory — Debugging Engineering

## 1. Debugging ไม่ใช่ Guessing

Workflow:

```text
reproduce → minimize → collect evidence → hypothesize
→ design experiment → root cause → fix → regression test
```

การแก้ symptomโดยไม่รู้ root causeสร้าง latent bugsได้.

## 2. Reproducibility

บันทึก exact command/input, build flags/commit, environmentที่เกี่ยวข้อง, expected vs actual, deterministic/intermittent และ first known good/bad versionถ้ามี.

## 3. Debug Builds

Baseline:

```bash
gcc -O0 -g3 -fno-omit-frame-pointer ...
```

แต่ production bugอาจต้อง debug binaryที่ `-O2`; อย่า assume `-O0` reproduce optimizer-sensitive bug.

## 4. DWARF

`-g` สร้าง DWARFใน ELF `.debug_*` sections. GDBใช้ mappingจาก addressesไป source lines/types/variables. Debug metadataไม่เปลี่ยน C semantics.

## 5. Breakpoints

```text
break function
break file.c:42
tbreak
condition N expression
ignore N count
```

Software breakpointทั่วไปใช้ trap mechanism. Breakpointsจำนวนมากอาจเปลี่ยน timingของ concurrent bugs.

## 6. Watchpoints

Hardware watchpointsหยุดเมื่อ memory locationถูก access/changeตามชนิดที่รองรับ. จำนวนจำกัดและ hardware-dependent. ต้องระวัง object lifetime/addressเปลี่ยน.

## 7. Frames / Backtraces

```text
backtrace
frame N
up / down
info args
info locals
```

คุณภาพ backtraceขึ้นกับ unwind info, stack integrity, optimization, frame pointers และ symbols.

## 8. Registers

```text
info registers
p/x $rax
p/x $rsp
x/16gx $rsp
```

Register stateเป็น evidenceใกล้ machineที่สุดแต่ต้องตีความด้วย instruction/ABI.

## 9. Memory Examine

GDB `x/NFU address`:
- N count
- F format เช่น x/d/i/s
- U unit b/h/w/g

ตัวอย่าง: `x/32bx ptr`, `x/8gx $rsp`, `x/10i $pc`, `x/s $rdi`.

## 10. Source + Assembly

```text
disassemble /m function
disassemble /r function
si
ni
```

เมื่อ source viewสับสนใน optimized build ให้กลับไป architectural state/disassembly.

## 11. step/next vs si/ni

`step/next` ทำงานระดับ source; `si/ni` ระดับ instruction. Optimizationทำให้ source steppingดู “กระโดด” ได้.

## 12. Optimized Debugging

ที่ `-O2`: variablesอาจ optimized out, functions inline, code reorder, constants propagate, tail callsเปลี่ยน stack. นี่ไม่ใช่ debuggerเสีย.

## 13. Signals

- SIGSEGV — invalid memory access/protection
- SIGABRT — abort/assertion
- SIGFPE — arithmetic exceptionบางประเภท
- SIGILL — illegal instruction
- SIGTRAP — breakpoint/trap

Signalบอก symptom class ไม่ใช่ root causeครบทั้งหมด.

## 14. Crash Site vs Root Cause

Use-after-freeอาจ crashหลัง freeนานแล้ว; out-of-bounds writeอาจ corrupt return addressแล้ว crashที่ ret. Faulting instructionไม่จำเป็นต้องเป็นจุดสร้าง bad state.

## 15. Core Dumps

Core dumpเป็น snapshotของ memory/register stateตอน crash. Availabilityขึ้นกับ `ulimit -c`, systemd-coredump, container/policy/storage. บน Fedoraมักใช้ `coredumpctl`เมื่อ configured.

## 16. Post-mortem

```bash
gdb ./program core
bt
info registers
frame N
x/...
```

ต้องใช้ executable/debug symbolsที่ match buildของ core.

## 17. Assertions

`assert` เหมาะกับ programmer invariantsใน testing/debug. `NDEBUG` disable standard assertionsได้ จึงไม่ใช้แทน validationของ runtime input.

## 18. Logging

Logที่ดีมี structured context, verbosityชัด, ไม่ log secrets และไม่เพิ่ม noiseจนเปลี่ยน timing bugโดยไม่รู้ตัว.

## 19. Sanitizers

ASanจับ memory errorsหลาย class; UBSanจับ undefined behaviorหลาย class. Clean sanitizer runไม่ใช่ proofว่าไม่มี bug.

## 20. Valgrind Preview

Valgrind/Memcheckเป็น optional toolและช้ากว่า instrumentation. Core chapterใช้ ASanเป็นหลัก.

## 21. Conditional Breakpoints

แทนหยุดทุก iteration ใช้ conditionเช่น `index == 999`. มี overheadแต่ isolate deterministic stateได้.

## 22. Breakpoint Command Lists

GDBสามารถ `commands ... silent ... printf ... continue` เพื่อ tracingขนาดเล็ก. ถ้าความถี่สูง toolsอื่นอาจเหมาะกว่า.

## 23. Catchpoints

GDBสามารถ catch signals/syscallsบน targetที่รองรับ เช่น `catch signal SIGSEGV`, `catch syscall write`.

## 24. Threads Preview

`info threads`, `thread N`, `thread apply all bt`. Schedules nondeterministicและ breakpointsเปลี่ยน timingได้.

## 25. Record / Reverse Preview

GDBบาง targetsรองรับ record/replay/reverse execution; ไม่เป็น required testเพราะ availabilityต่างกัน.

## 26. Binary Without Source

ยังใช้ `info files`, `info functions`, `disassemble`, `break *ADDRESS`, `x/i $pc` ได้กับ course binaries.

## 27. Stripped Binary

เมื่อ full symtab/DWARFหาย GDBยังทำ machine-level debuggingและอาจเห็น dynamic symbolsบางส่วน. “ไม่มี debug symbols” ไม่เท่ากับ “ไม่มี symbolsใดเลย”.

## 28. Shared Libraries

`info sharedlibrary`, pending breakpointsช่วย libraryที่โหลดทีหลัง. ASLRทำ runtime addressเปลี่ยน; debuggerใช้ mappings/symbol relocation.

## 29. Startup Debugging

`starti` เริ่มที่ instructionแรก; break `_start`, `main`, shared function และใช้ `info proc mappings` เชื่อม ELFกับ runtime.

## 30. Stack Corruption

Nonsense backtrace, invalid return, canary failureอาจมาจาก earlier out-of-bounds write. ASan/stack protectorช่วย narrow.

## 31. Heap Corruption

Invalid free/double-free/UAFอาจถูก allocatorหรือ ASanจับคนละจุด. Allocator abort siteไม่จำเป็นต้องเป็น original bad write.

## 32. Optimized Assembly Workflow

ใช้ ABI knowledge: identify inputs → track registers → map memory objects → follow branches → inspect calls → validate hypothesisด้วย breakpoint.

## 33. Regression Test

Fixยังไม่จบจนมี testที่ failก่อน fixและ passหลัง fixถ้าทำได้. Testควร capture behavioral contract ไม่ใช่ implementation detailที่ไม่จำเป็น.

## 34. Evidence Hierarchy

Strong: reproducible input, exact state, sanitizer report, minimized test, mechanism-explaining diff. Weak: “น่าจะ”, random edits, one-off timing.

## 35. Debugging Checklist

Can I reproduce? What changed? Where is first divergence? What invariant broke? Which write/call created bad state? Can I prove it? Can I fix without hiding symptom? Can I add regression coverage?

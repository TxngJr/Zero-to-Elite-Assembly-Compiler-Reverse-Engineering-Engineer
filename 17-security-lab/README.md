# Chapter 17 — Defensive Security Lab

บทนี้ฝึก **defensive vulnerability research** บน code/binariesที่อยู่ใน repositoryนี้เท่านั้น.

Workflow:

```text
find a defect
→ reproduce locally
→ sanitizer/debugger evidence
→ minimize input
→ root cause
→ patch
→ regression
→ fuzz fixed code
→ defensive report
```

ไม่สอน unauthorized exploitation, credential theft, persistence, malicious deployment หรือการซ่อน activity.

ทุก bug demoเป็น compile-time injected bugใน course project และ testsปกติใช้ fixed implementation.

## Navigation
- [Objectives](OBJECTIVES.md)
- [Prerequisites](PREREQUISITES.md)
- [Theory](THEORY.md)
- [Labs](LABS.md)
- [Exercises](EXERCISES.md)
- [Challenges](CHALLENGES.md)
- [Common mistakes](COMMON_MISTAKES.md)
- [Mastery test](MASTERY_TEST.md)
- [Answers / hints](ANSWERS.md)

**Previous:** [Chapter 16 — Reverse Engineering](../16-reverse-engineering/README.md)  
**Next:** [Chapter 18 — Final Capstone](../18-capstone/README.md)

```bash
make clean test
make sanitize
make fuzz
```

Projects:
- `projects/parser-lab/` — bounds-checking/root-cause/patch exercise
- `projects/integer-lab/` — checked integer arithmetic
- `projects/fuzz-lab/` — deterministic in-process fuzz smoke test
- `projects/crash-triage/` — sanitizer-log summarizer

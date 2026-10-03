# Chapter 17 — Defensive Security Lab

บทนี้ฝึก **defensive vulnerability research** บน code/binariesที่อยู่ใน repositoryนี้เท่านั้น.

เป้าหมาย:

```text
find a defect
→ reproduce locally
→ collect sanitizer/debugger evidence
→ minimize input
→ identify root cause
→ patch
→ add regression test
→ fuzz fixed code
→ document impact without weaponizing
```

บทนี้ไม่สอน:
- bypass authentication/licensing
- persistence
- credential theft
- malware deployment
- exploitation of third-party systems
- hiding activity

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
**Next:** Chapter 18 — Final Capstone (**not implemented yet**)

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

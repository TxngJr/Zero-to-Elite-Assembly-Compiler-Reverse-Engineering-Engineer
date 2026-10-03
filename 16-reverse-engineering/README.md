# Chapter 16 — Reverse Engineering

บทนี้ฝึก reverse engineering แบบมีสิทธิ์และควบคุมได้ โดยใช้ **course-owned binariesที่สร้างจาก sourceใน repositoryนี้เท่านั้น**.

เป้าหมายไม่ใช่ “เดารหัสผ่าน” หรือ bypass ระบบ แต่คือสร้างความสามารถในการอ่าน binaryเพื่อ:

- debugging
- compatibility
- incident/root-cause analysis
- malware-analysis fundamentalsเชิง defensiveในอนาคต
- patch review
- compiler/codegen understanding
- recovery of program structure when source is unavailable

Workflow:

```text
provenance / hash
→ file & ELF metadata
→ symbols / sections / strings
→ disassembly
→ functions / control flow
→ data-flow & structures
→ dynamic observation
→ hypothesis
→ evidence-backed reconstruction
```

## Scope Rule

วิเคราะห์เฉพาะ:
- binariesจาก `projects/challenge-suite/`
- softwareที่คุณเขียนเอง
- open-source/training/CTF binariesที่อนุญาตชัดเจน

หลีกเลี่ยงการใช้บทนี้เพื่อ bypass authentication/licensing, ขโมยข้อมูล, persistence หรือ unauthorized access.

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

**Previous:** [Chapter 15 — Advanced OS](../15-advanced-os/README.md)  
**Next:** [Chapter 17 — Security Lab](../17-security-lab/README.md)

```bash
make clean test
make build-challenges
python3 projects/binary-report/binary_report.py build/challenges/control-o2
python3 projects/cfg-extract/cfg_extract.py build/challenges/control-o0
```

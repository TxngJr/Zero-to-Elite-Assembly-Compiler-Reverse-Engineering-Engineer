# Labs

1. Draw the complete source→CPU pipeline from memory.
2. Run `make clean test`.
3. Inspect `build/capstone.ir`; identify loop/branch/call blocks.
4. Inspect `build/capstone.s`; annotate prologues, calls and stack use.
5. Inspect `build/capstone.elf.txt`; identify ELF type, entry and machine.
6. Locate `fact` and `sum8` in disassembly.
7. Explain how 8 arguments cross the SysV ABI boundary.
8. Inspect `binary-report.json`; separate raw observations from interpretation.
9. Inspect `cfg.txt`; identify function-call edges.
10. Hash capstone executable manually and compare with manifest.
11. Inspect copied EliteOS64 kernel header/sections.
12. Re-run Multiboot2 validator manually.
13. Explain why kernel artifact is ELF64 even though entry begins with 32-bit code.
14. Explain Chapter 14 vs Chapter 15 responsibilities.
15. Trace COW simulator parent/child frame ownership.
16. Trace scheduler simulator ready/running/done states.
17. Trace pipe wrap-around manually.
18. Trace VFS lookup `/etc/motd`.
19. Run Chapter 17 fixed parser/fuzzer tests.
20. Run sanitizer-demo separately and write root-cause note.
21. Perform static RE on capstone-app without looking at capstone.el.
22. Compare your reconstructed pseudocode with source.
23. Complete REPORT_TEMPLATE.md.
24. Complete PORTFOLIO_TEMPLATE.md.
25. Perform oral defense using questions in MASTERY_TEST.md.

# Labs

1. Build challenge suite; hash binariesด้วย sha256sum.
2. Triage control-o0ด้วย file/readelf.
3. Compare control-o0 vs control-o2 section/function sizes.
4. Compare PIE vs non-PIE ELF type.
5. Compare symbol tableก่อน/หลัง strip.
6. Find strings and locate xrefs via disassembly.
7. Reconstruct `classify` switchจาก O0.
8. Reconstruct same functionจาก O2โดยไม่เปิด sourceจนจบ.
9. Analyze array strideใน structs binary.
10. Infer field offsetsใน Record struct.
11. Identify recursive function call pattern.
12. Run binary-report tool and annotate evidence.
13. Run cfg-extract; identify loop back edge.
14. Use GDB breakpoint on `sum_records` in unstripped course binary.
15. Inspect RDI/RSI arguments and memory.
16. Compare runtime PIE mappingsกับ link-time addresses.
17. Write pseudocode for one stripped function.
18. Compare your pseudocodeกับ sourceและบันทึก inference mistakes.
19. Write one-page RE report using REPORT_TEMPLATE.md.
20. Explain what static/dynamic evidence each conclusion uses.

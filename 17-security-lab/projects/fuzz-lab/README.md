# Fuzz Lab

มีสองระดับที่ต้องแยกให้ชัด:

1. `fuzz_driver.c` — deterministic pseudo-random **smoke/stress test** 5,000 cases สำหรับ CI ที่ reproducible
2. `libfuzzer_target.c` — coverage-guided libFuzzer target จริงสำหรับ local authorized lab

```bash
make test       # deterministic smoke
make sanitize   # same smoke under ASan/UBSan
make libfuzzer  # clang + coverage-guided libFuzzer, 2000 runs
```

การไม่มี crash ไม่ได้แปลว่า parser ปลอดภัย. เป้าหมายคือฝึก harness, corpus, sanitizer evidence, minimization และ regression workflow.

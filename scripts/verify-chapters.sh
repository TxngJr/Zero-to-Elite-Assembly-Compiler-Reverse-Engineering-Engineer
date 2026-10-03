#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

required=(
  README.md COURSE_MAP.md STUDY_GUIDE.md GLOSSARY.md TROUBLESHOOTING.md
  00-linux-lab/README.md 00-linux-lab/THEORY.md 00-linux-lab/LABS.md 00-linux-lab/MASTERY_TEST.md
  01-computer-foundations/README.md 01-computer-foundations/THEORY.md 01-computer-foundations/LABS.md 01-computer-foundations/MASTERY_TEST.md
  02-c-machine-model/README.md 02-c-machine-model/THEORY.md 02-c-machine-model/LABS.md 02-c-machine-model/MASTERY_TEST.md
  03-x86-64-assembly/README.md 03-x86-64-assembly/THEORY.md 03-x86-64-assembly/LABS.md 03-x86-64-assembly/MASTERY_TEST.md
  04-abi-syscalls/README.md 04-abi-syscalls/THEORY.md 04-abi-syscalls/LABS.md 04-abi-syscalls/MASTERY_TEST.md
  05-computer-architecture/README.md 05-computer-architecture/THEORY.md 05-computer-architecture/LABS.md 05-computer-architecture/MASTERY_TEST.md
  06-elf/README.md 06-elf/THEORY.md 06-elf/LABS.md 06-elf/MASTERY_TEST.md
  07-linker-loader/README.md 07-linker-loader/THEORY.md 07-linker-loader/LABS.md 07-linker-loader/MASTERY_TEST.md
  08-debugging/README.md 08-debugging/THEORY.md 08-debugging/LABS.md 08-debugging/MASTERY_TEST.md
  09-compiler-frontend/README.md 09-compiler-frontend/THEORY.md 09-compiler-frontend/LABS.md 09-compiler-frontend/MASTERY_TEST.md
  10-compiler-ir/README.md 10-compiler-ir/THEORY.md 10-compiler-ir/LABS.md 10-compiler-ir/MASTERY_TEST.md
  11-compiler-backend/README.md 11-compiler-backend/THEORY.md 11-compiler-backend/LABS.md 11-compiler-backend/MASTERY_TEST.md
  12-my-compiler/README.md 12-my-compiler/THEORY.md 12-my-compiler/LABS.md 12-my-compiler/MASTERY_TEST.md
  13-os-foundations/README.md 13-os-foundations/THEORY.md 13-os-foundations/LABS.md 13-os-foundations/MASTERY_TEST.md
  14-my-os/README.md 14-my-os/THEORY.md 14-my-os/LABS.md 14-my-os/MASTERY_TEST.md
  15-advanced-os/README.md 15-advanced-os/THEORY.md 15-advanced-os/LABS.md 15-advanced-os/MASTERY_TEST.md
  16-reverse-engineering/README.md 16-reverse-engineering/THEORY.md 16-reverse-engineering/LABS.md 16-reverse-engineering/MASTERY_TEST.md
  17-security-lab/README.md 17-security-lab/THEORY.md 17-security-lab/LABS.md 17-security-lab/MASTERY_TEST.md
  18-capstone/README.md 18-capstone/THEORY.md 18-capstone/LABS.md 18-capstone/MASTERY_TEST.md
  18-capstone/FINAL_CHECKLIST.md 18-capstone/PORTFOLIO_TEMPLATE.md 18-capstone/REPORT_TEMPLATE.md
)

fail=0

for f in "${required[@]}"; do
  if [[ -s "$ROOT/$f" ]]; then
    echo "[OK] $f"
  else
    echo "[FAIL] missing/empty $f"
    fail=1
  fi
done

for script in   "$ROOT"/scripts/*.sh   "$ROOT"/*/tests/*.sh   "$ROOT"/*/projects/*/*.sh   "$ROOT"/*/scripts/*.sh
do
  [[ -e "$script" ]] || continue
  bash -n "$script" || fail=1
done

for py in   "$ROOT"/09-compiler-frontend/projects/elite-frontend/*.py   "$ROOT"/10-compiler-ir/projects/elite-ir/*.py   "$ROOT"/11-compiler-backend/projects/elite-backend/*.py   "$ROOT"/12-my-compiler/projects/elitec/*.py   "$ROOT"/13-os-foundations/projects/page-walk-sim/*.py   "$ROOT"/14-my-os/tests/*.py   "$ROOT"/15-advanced-os/projects/vm-cow-sim/*.py   "$ROOT"/16-reverse-engineering/projects/binary-report/*.py   "$ROOT"/16-reverse-engineering/projects/cfg-extract/*.py   "$ROOT"/17-security-lab/projects/crash-triage/*.py   "$ROOT"/18-capstone/projects/final-audit/*.py
do
  [[ -e "$py" ]] || continue
  python3 -m py_compile "$py" || fail=1
done

for ch in   00-linux-lab   01-computer-foundations   02-c-machine-model   03-x86-64-assembly   04-abi-syscalls   05-computer-architecture   06-elf   07-linker-loader   08-debugging   09-compiler-frontend   10-compiler-ir   11-compiler-backend   12-my-compiler   13-os-foundations   14-my-os   15-advanced-os   16-reverse-engineering   17-security-lab   18-capstone
do
  echo "--- testing $ch ---"
  if ! make -C "$ROOT/$ch" clean test; then
    fail=1
  fi
done

if (( fail )); then
  echo '[FAIL] Chapter verification failed.'
  exit 1
fi

echo '[OK] Chapters 00–18 verified. Course implementation complete.'

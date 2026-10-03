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
)
fail=0
for f in "${required[@]}"; do
  if [[ -s "$ROOT/$f" ]]; then echo "[OK] $f"; else echo "[FAIL] missing/empty $f"; fail=1; fi
done

for script in "$ROOT"/scripts/*.sh "$ROOT"/*/tests/*.sh "$ROOT"/*/projects/*/*.sh; do
  [[ -e "$script" ]] || continue
  bash -n "$script" || fail=1
done

for ch in 00-linux-lab 01-computer-foundations 02-c-machine-model 03-x86-64-assembly 04-abi-syscalls 05-computer-architecture; do
  echo "--- testing $ch ---"
  if ! make -C "$ROOT/$ch" clean test; then fail=1; fi
done

if (( fail )); then echo '[FAIL] Chapter verification failed.'; exit 1; fi
echo '[OK] Chapters 00–05 verified.'

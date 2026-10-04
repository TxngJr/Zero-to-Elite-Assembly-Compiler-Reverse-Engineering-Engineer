#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
fail=0

echo '=== Course quality structure ==='
if ! python3 "$ROOT/scripts/check-course-quality.py"; then
  fail=1
fi

echo '=== Shell syntax ==='
for script in   "$ROOT"/scripts/*.sh   "$ROOT"/*/tests/*.sh   "$ROOT"/*/projects/*/*.sh   "$ROOT"/*/scripts/*.sh
do
  [[ -e "$script" ]] || continue
  bash -n "$script" || fail=1
done

echo '=== Python syntax ==='
for py in   "$ROOT"/scripts/*.py   "$ROOT"/09-compiler-frontend/projects/elite-frontend/*.py   "$ROOT"/09-compiler-frontend/tests/*.py   "$ROOT"/10-compiler-ir/projects/elite-ir/*.py   "$ROOT"/10-compiler-ir/tests/*.py   "$ROOT"/11-compiler-backend/projects/elite-backend/*.py   "$ROOT"/12-my-compiler/projects/elitec/*.py   "$ROOT"/13-os-foundations/projects/page-walk-sim/*.py   "$ROOT"/14-my-os/tests/*.py   "$ROOT"/15-advanced-os/projects/vm-cow-sim/*.py   "$ROOT"/16-reverse-engineering/projects/binary-report/*.py   "$ROOT"/16-reverse-engineering/projects/cfg-extract/*.py   "$ROOT"/17-security-lab/projects/crash-triage/*.py   "$ROOT"/18-capstone/projects/final-audit/*.py
do
  [[ -e "$py" ]] || continue
  python3 -m py_compile "$py" || fail=1
done

chapters=(
  00-linux-lab
  01-computer-foundations
  02-c-machine-model
  03-x86-64-assembly
  04-abi-syscalls
  05-computer-architecture
  06-elf
  07-linker-loader
  08-debugging
  09-compiler-frontend
  10-compiler-ir
  11-compiler-backend
  12-my-compiler
  13-os-foundations
  14-my-os
  15-advanced-os
  16-reverse-engineering
  17-security-lab
  18-capstone
)

for ch in "${chapters[@]}"; do
  echo "--- automated tests: $ch ---"
  if ! make -C "$ROOT/$ch" clean test; then
    fail=1
  fi
done

if (( fail )); then
  echo '[FAIL] Automated repository checks failed.'
  exit 1
fi

echo '[OK] Automated repository checks for Chapters 00–18 passed.'
echo '[INFO] This result does not certify learner mastery, production readiness, security, or hardware-wide OS compatibility.'
echo '[INFO] Run make -C 14-my-os qemu-test for the separate runtime boot/PIT gate.'

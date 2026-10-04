#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PY=${PYTHON:-python3}
CC=${CC:-gcc}

rm -rf "$ROOT/build"
mkdir -p "$ROOT/build"

$PY "$ROOT/projects/final-audit/final_audit.py" "$CC" > "$ROOT/build/audit.log"

test -x "$ROOT/build/capstone-app"
test -s "$ROOT/build/capstone.ir"
test -s "$ROOT/build/capstone.s"
test -s "$ROOT/build/capstone.elf.txt"
test -s "$ROOT/build/capstone.dis"
test -s "$ROOT/build/binary-report.json"
test -s "$ROOT/build/cfg.txt"
test -s "$ROOT/build/eliteos64-kernel.elf"
test -s "$ROOT/build/manifest.json"
test -s "$ROOT/build/audit-summary.json"

grep -q '^\[OK\] final capstone audit:' "$ROOT/build/audit.log"
grep -q '"status": "passed"' "$ROOT/build/audit-summary.json"
grep -q '"scope": "course-owned artifacts and defensive tests only"' "$ROOT/build/audit-summary.json"
grep -q '"qemu_runtime"' "$ROOT/build/audit-summary.json"
grep -Eq '"status": "(passed|skipped)"' "$ROOT/build/audit-summary.json"
grep -q '"build/capstone-app"' "$ROOT/build/manifest.json"
grep -q '"build/eliteos64-kernel.elf"' "$ROOT/build/manifest.json"
grep -q 'ELF64' "$ROOT/build/capstone.elf.txt"
grep -q '<fact>' "$ROOT/build/capstone.dis"
grep -q -- '--call-->' "$ROOT/build/cfg.txt"
grep -q 'multiboot2 header OK' "$ROOT/build/multiboot.txt"

$PY -m py_compile "$ROOT/projects/final-audit/final_audit.py"

echo '[OK] chapter 18 final capstone'

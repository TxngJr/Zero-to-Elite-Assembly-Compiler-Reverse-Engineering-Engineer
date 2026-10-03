#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CC=${CC:-gcc}
PY=${PYTHON:-python3}

make -C "$ROOT/projects/challenge-suite" clean all CC="$CC"

"$ROOT/build/challenges/control-o0" 5 > "$ROOT/build/control.out"
grep -q '^91$' "$ROOT/build/control.out"

"$ROOT/build/challenges/records-o2" > "$ROOT/build/records.out"
grep -q '^5$' "$ROOT/build/records.out"

$PY "$ROOT/projects/binary-report/binary_report.py" "$ROOT/build/challenges/control-o0" > "$ROOT/build/report.json"
grep -q '"sha256"' "$ROOT/build/report.json"
grep -q 'ELF 64-bit' "$ROOT/build/report.json"

$PY "$ROOT/projects/cfg-extract/cfg_extract.py" "$ROOT/build/challenges/control-o0" > "$ROOT/build/cfg.txt"
grep -q -- '--call-->' "$ROOT/build/cfg.txt"

file "$ROOT/build/challenges/control-stripped" > "$ROOT/build/stripped.txt"
grep -qi 'stripped' "$ROOT/build/stripped.txt"

$PY -m py_compile "$ROOT/projects/binary-report/binary_report.py"
$PY -m py_compile "$ROOT/projects/cfg-extract/cfg_extract.py"

echo '[OK] chapter 16 reverse-engineering course binaries'

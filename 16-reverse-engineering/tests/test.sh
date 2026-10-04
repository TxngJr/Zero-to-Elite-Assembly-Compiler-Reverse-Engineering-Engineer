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

$PY "$ROOT/projects/binary-report/binary_report.py"   "$ROOT/build/challenges/control-o0" > "$ROOT/build/report.json"
grep -q '"sha256"' "$ROOT/build/report.json"
grep -q 'ELF 64-bit' "$ROOT/build/report.json"
grep -q '"status": "ok"' "$ROOT/build/report.json"

$PY "$ROOT/projects/cfg-extract/cfg_extract.py"   "$ROOT/build/challenges/control-o0" > "$ROOT/build/cfg.txt"
grep -q '^function ' "$ROOT/build/cfg.txt"
grep -q 'block 0x' "$ROOT/build/cfg.txt"
grep -q -- '--call-->' "$ROOT/build/cfg.txt"
grep -Eq -- '--(branch|fallthrough)-->' "$ROOT/build/cfg.txt"

$PY "$ROOT/projects/cfg-extract/cfg_extract.py" --json   "$ROOT/build/challenges/control-o0" > "$ROOT/build/cfg.json"
grep -q '"blocks"' "$ROOT/build/cfg.json"
grep -q '"edges"' "$ROOT/build/cfg.json"

file "$ROOT/build/challenges/control-stripped" > "$ROOT/build/stripped.txt"
grep -qi 'stripped' "$ROOT/build/stripped.txt"

# Required ELF tools must fail the report on a non-ELF input.
printf 'not an elf\n' > "$ROOT/build/not-elf.txt"
set +e
$PY "$ROOT/projects/binary-report/binary_report.py"   "$ROOT/build/not-elf.txt" >/dev/null 2>"$ROOT/build/not-elf.err"
s=$?
set -e
test "$s" -ne 0
grep -q 'binary-report: error:' "$ROOT/build/not-elf.err"

$PY -m py_compile   "$ROOT/projects/binary-report/binary_report.py"   "$ROOT/projects/cfg-extract/cfg_extract.py"

echo '[OK] chapter 16 RE tooling validates failures and real CFG blocks'

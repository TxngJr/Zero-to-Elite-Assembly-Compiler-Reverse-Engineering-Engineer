#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CC=${CC:-gcc}
PY=${PYTHON:-python3}

make -C "$ROOT/projects/parser-lab" clean test CC="$CC"
make -C "$ROOT/projects/integer-lab" clean test CC="$CC"
make -C "$ROOT/projects/fuzz-lab" clean test CC="$CC"

$PY "$ROOT/projects/crash-triage/triage.py"   "$ROOT/projects/crash-triage/sample_asan.txt" > "$ROOT/triage.out"
grep -q 'sanitizer_error=stack-buffer-overflow' "$ROOT/triage.out"
grep -q 'first_frame=parse_packet' "$ROOT/triage.out"

$PY -m py_compile "$ROOT/projects/crash-triage/triage.py"
rm -f "$ROOT/triage.out"
echo '[OK] chapter 17 defensive security labs'

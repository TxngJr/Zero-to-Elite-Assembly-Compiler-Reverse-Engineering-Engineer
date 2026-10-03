#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PY=${PYTHON:-python3}
CC=${CC:-gcc}

$PY "$ROOT/projects/page-walk-sim/page_walk.py" split 0x7fffffffffff > "$ROOT/split.out"
grep -q 'pml4=255' "$ROOT/split.out"
grep -q 'offset=4095' "$ROOT/split.out"
$PY "$ROOT/projects/page-walk-sim/page_walk.py" demo > "$ROOT/demo.out"
grep -q '0x200123' "$ROOT/demo.out"
grep -q '0x900456' "$ROOT/demo.out"

set +e
$PY "$ROOT/projects/page-walk-sim/page_walk.py" split 0x0000800000000000 >/dev/null 2>&1
s=$?
set -e
test "$s" -ne 0

make -C "$ROOT/projects/descriptor-lab" clean test CC="$CC"
$PY -m py_compile "$ROOT/projects/page-walk-sim/page_walk.py"
rm -f "$ROOT/split.out" "$ROOT/demo.out"
echo '[OK] chapter 13 OS foundations'

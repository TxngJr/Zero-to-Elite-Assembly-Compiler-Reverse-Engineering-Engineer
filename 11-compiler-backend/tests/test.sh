#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PY=${PYTHON:-python3}
CC=${CC:-gcc}
TOOL="$ROOT/projects/elite-backend/elite_backend.py"
mkdir -p "$ROOT/build"
compile_run_status() {
  local src=$1 expected=$2 name=$3
  $PY "$TOOL" "$src" -o "$ROOT/build/$name.s"
  $CC "$ROOT/build/$name.s" -o "$ROOT/build/$name"
  set +e
  "$ROOT/build/$name"
  local s=$?
  set -e
  test "$s" -eq "$expected"
}
compile_run_status "$ROOT/examples/return42.el" 42 return42
compile_run_status "$ROOT/examples/complex.el" 0 complex
compile_run_status "$ROOT/examples/loop.el" 55 loop
compile_run_status "$ROOT/examples/short_circuit.el" 0 short-circuit
$PY "$TOOL" --opt "$ROOT/examples/return42.el" -o "$ROOT/build/opt.s"
grep -q '^\.global main' "$ROOT/build/opt.s"
objdump -d -Mintel "$ROOT/build/complex" > "$ROOT/build/complex.dis"
grep -q '<fact>' "$ROOT/build/complex.dis"
$PY "$ROOT/tests/test_linear_scan.py"
$PY "$ROOT/projects/linear-scan/linear_scan.py" --json > "$ROOT/build/linear-scan.json"
grep -q '"spilled": true' "$ROOT/build/linear-scan.json"
$PY -m py_compile "$TOOL" "$ROOT/projects/linear-scan/linear_scan.py" "$ROOT/tests/test_linear_scan.py"
echo '[OK] chapter 11 backend + linear-scan allocation lab'

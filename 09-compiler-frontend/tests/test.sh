#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PY=${PYTHON:-python3}
TOOL="$ROOT/projects/elite-frontend/elite_frontend.py"

$PY "$ROOT/tests/test_frontend.py"

$PY "$TOOL" --check "$ROOT/examples/valid.el" > "$ROOT/check.out"
grep -q '^OK$' "$ROOT/check.out"
$PY "$TOOL" --tokens "$ROOT/examples/valid.el" > "$ROOT/tokens.out"
grep -q '^FN' "$ROOT/tokens.out"
$PY "$TOOL" --ast "$ROOT/examples/control.el" > "$ROOT/ast.out"
grep -q '"functions"' "$ROOT/ast.out"

rm -f "$ROOT/check.out" "$ROOT/tokens.out" "$ROOT/ast.out"
$PY -m py_compile "$TOOL" "$ROOT/tests/test_frontend.py"
echo '[OK] chapter 09 frontend semantic tests'

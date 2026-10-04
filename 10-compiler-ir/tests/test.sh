#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PY=${PYTHON:-python3}
TOOL="$ROOT/projects/elite-ir/elite_ir.py"

$PY "$ROOT/tests/test_ir.py"

$PY "$TOOL" --ir "$ROOT/examples/loop.el" > "$ROOT/ir.txt"
grep -q 'cjump' "$ROOT/ir.txt"
grep -q 'while_body' "$ROOT/ir.txt"

$PY "$TOOL" --dom "$ROOT/examples/diamond.el" > "$ROOT/dom.txt"
grep -q '^function main$' "$ROOT/dom.txt"

$PY "$TOOL" --live "$ROOT/examples/loop.el" > "$ROOT/live.txt"
grep -q 'out=' "$ROOT/live.txt"

$PY "$ROOT/tests/test_ssa.py"
$PY "$TOOL" --phi-candidates "$ROOT/examples/diamond.el" > "$ROOT/phi.txt"
grep -q 'x' "$ROOT/phi.txt"
$PY "$TOOL" --ssa "$ROOT/examples/diamond.el" > "$ROOT/ssa.txt"
grep -q ' = phi ' "$ROOT/ssa.txt"

$PY "$TOOL" --opt "$ROOT/examples/fold.el" > "$ROOT/opt.txt"
grep -q 'const 43' "$ROOT/opt.txt"

$PY -m py_compile "$TOOL" "$ROOT/projects/elite-ir/elite_ssa.py" "$ROOT/tests/test_ir.py" "$ROOT/tests/test_ssa.py"
rm -f "$ROOT"/{ir,dom,live,phi,ssa,opt}.txt
echo '[OK] chapter 10 IR semantic tests'

#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PY=${PYTHON:-python3}
TOOL="$ROOT/projects/elite-ir/elite_ir.py"
$PY "$TOOL" --ir "$ROOT/examples/loop.el" > "$ROOT/ir.txt"
grep -q 'cjump' "$ROOT/ir.txt"
grep -q 'while_body' "$ROOT/ir.txt"
$PY "$TOOL" --dom "$ROOT/examples/diamond.el" | grep -q 'function main'
$PY "$TOOL" --live "$ROOT/examples/loop.el" | grep -q 'out='
$PY "$TOOL" --ssa "$ROOT/examples/diamond.el" | grep -q 'x'
$PY "$TOOL" --opt "$ROOT/examples/fold.el" | grep -q 'const 43'
$PY -m py_compile "$TOOL"
rm -f "$ROOT/ir.txt"
echo '[OK] chapter 10 IR'

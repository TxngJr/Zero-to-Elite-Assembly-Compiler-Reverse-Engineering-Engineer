#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PY=${PYTHON:-python3}
TOOL="$ROOT/projects/elite-frontend/elite_frontend.py"
$PY "$TOOL" --check "$ROOT/examples/valid.el" | grep -q '^OK$'
$PY "$TOOL" --tokens "$ROOT/examples/valid.el" | grep -q '^FN'
$PY "$TOOL" --ast "$ROOT/examples/control.el" | grep -q '"functions"'
set +e
$PY "$TOOL" --check "$ROOT/examples/type_error.el" >/dev/null 2>&1
s=$?
set -e
test "$s" -ne 0
$PY -m py_compile "$TOOL"
echo '[OK] chapter 09 frontend'

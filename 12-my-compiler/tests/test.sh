#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
PY=${PYTHON:-python3}
CC=${CC:-gcc}
ELITEC="$ROOT/projects/elitec/elitec.py"
mkdir -p "$ROOT/build"

$PY "$ELITEC" --check "$ROOT/examples/factorial.el" > "$ROOT/build/check.txt"
grep -q '^OK$' "$ROOT/build/check.txt"

$PY "$ELITEC" --emit tokens "$ROOT/examples/return42.el" > "$ROOT/build/tokens.txt"
grep -q '^FN' "$ROOT/build/tokens.txt"

$PY "$ELITEC" --emit ast "$ROOT/examples/factorial.el" > "$ROOT/build/ast.json"
grep -q '"functions"' "$ROOT/build/ast.json"

$PY "$ELITEC" --emit ir "$ROOT/examples/factorial.el" > "$ROOT/build/factorial.ir"
grep -q 'cjump' "$ROOT/build/factorial.ir"

$PY "$ELITEC" --emit asm "$ROOT/examples/factorial.el" > "$ROOT/build/factorial.s"
grep -q '^\.global fact' "$ROOT/build/factorial.s"

$PY "$ELITEC" --cc "$CC" "$ROOT/examples/return42.el" -o "$ROOT/build/return42"
set +e
"$ROOT/build/return42"
s=$?
set -e
test "$s" -eq 42

$PY "$ELITEC" --cc "$CC" "$ROOT/examples/factorial.el" -o "$ROOT/build/factorial"
"$ROOT/build/factorial"

$PY "$ELITEC" --cc "$CC" "$ROOT/examples/sum8.el" -o "$ROOT/build/sum8"
"$ROOT/build/sum8"

$PY "$ELITEC" --cc "$CC" "$ROOT/examples/short_circuit.el" -o "$ROOT/build/short"
"$ROOT/build/short"

$PY "$ELITEC" --opt --cc "$CC" "$ROOT/examples/factorial.el" -o "$ROOT/build/factorial-opt"
"$ROOT/build/factorial-opt"

set +e
$PY "$ELITEC" --check "$ROOT/examples/type_error.el" >"$ROOT/build/type.out" 2>"$ROOT/build/type.err"
s=$?
set -e
test "$s" -ne 0
! grep -q 'Traceback' "$ROOT/build/type.err"

file "$ROOT/build/factorial" > "$ROOT/build/file.txt"
grep -qi 'ELF' "$ROOT/build/file.txt"
readelf -h "$ROOT/build/factorial" > "$ROOT/build/elf-header.txt"
grep -q 'X86-64' "$ROOT/build/elf-header.txt"

$PY -m py_compile "$ELITEC"
echo '[OK] chapter 12 EliteC end-to-end'

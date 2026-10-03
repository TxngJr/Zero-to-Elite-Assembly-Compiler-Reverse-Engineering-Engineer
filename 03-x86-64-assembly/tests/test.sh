#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
for src in "$ROOT"/examples/*.s; do
  name=$(basename "${src%.s}")
  "$cc" -g -no-pie "$src" -o "$ROOT/build/$name"
done
set +e
"$ROOT/build/exit_code"; s=$?
set -e
[[ $s -eq 42 ]]
"$ROOT/build/branches"
"$ROOT/build/addressing"
"$ROOT/build/bitwise"
set +e
"$ROOT/build/arithmetic"; s=$?
set -e
[[ $s -eq 50 ]]
make -C "$ROOT/projects/array-kernels" clean test CC="$cc"
objdump -d -Mintel "$ROOT/build/addressing" | grep -q 'lea'
echo '[OK] chapter 03 assembly examples/projects'

#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
flags=(-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g)
for src in "$ROOT"/examples/*.c; do
  base=$(basename "${src%.c}")
  out="$ROOT/build/$base"
  "$cc" "${flags[@]}" "$src" -o "$out"
  if [[ "$base" == show_integer_bits ]]; then "$out" 65 >/dev/null; else "$out" >/dev/null; fi
done
make -C "$ROOT/projects/binary-playground" clean test
make -C "$ROOT/projects/memory-viewer" clean test
echo '[OK] chapter 01 examples/projects compile and run'

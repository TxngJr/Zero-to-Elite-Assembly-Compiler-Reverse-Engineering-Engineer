#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
flags=(-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g)
for src in "$ROOT"/examples/*.c; do
  base=$(basename "${src%.c}")
  [[ "$base" == buggy_bounds ]] && continue
  "$cc" "${flags[@]}" "$src" -o "$ROOT/build/$base"
  "$ROOT/build/$base" >/dev/null
done
"$cc" "${flags[@]}" -I"$ROOT/examples/multifile" -c "$ROOT/examples/multifile/main.c" -o "$ROOT/build/multi-main.o"
"$cc" "${flags[@]}" -I"$ROOT/examples/multifile" -c "$ROOT/examples/multifile/math_utils.c" -o "$ROOT/build/math-utils.o"
"$cc" "$ROOT/build/multi-main.o" "$ROOT/build/math-utils.o" -o "$ROOT/build/multifile"
[[ "$("$ROOT/build/multifile")" == 42 ]]
for project in mini-string dynamic-array arena-allocator hexdump; do
  make -C "$ROOT/projects/$project" clean test
done
"$cc" "${flags[@]}" -DFIXED "$ROOT/examples/buggy_bounds.c" -o "$ROOT/build/bounds-fixed"
"$ROOT/build/bounds-fixed" >/dev/null
echo '[OK] chapter 02 examples/projects compile and run'

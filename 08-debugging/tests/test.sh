#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
flags=(-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g -fno-omit-frame-pointer)

for src in debug_target optimized crash_target assert_target; do
  "$cc" "${flags[@]}" "$ROOT/examples/$src.c" -o "$ROOT/build/$src"
done

test "$("$ROOT/build/debug_target")" = 'total=150'
test "$("$ROOT/build/optimized")" = '52'
test "$("$ROOT/build/crash_target")" = 'safe path'
test "$("$ROOT/build/assert_target")" = '49'

if command -v gdb >/dev/null 2>&1; then
  gdb -q -batch -x "$ROOT/tests/inspect.gdb" "$ROOT/build/debug_target" > "$ROOT/build/gdb.out"
  grep -q COMPUTE_TOTAL_BREAK "$ROOT/build/gdb.out"
else
  echo '[OPTIONAL] gdb not available; batch-debug test skipped'
fi

make -C "$ROOT/projects/debug-lab" clean test CC="$cc"
if command -v gdb >/dev/null 2>&1; then
  make -C "$ROOT/projects/debug-lab" gdb-test CC="$cc"
fi

echo '[OK] chapter 08 debugging examples/projects'

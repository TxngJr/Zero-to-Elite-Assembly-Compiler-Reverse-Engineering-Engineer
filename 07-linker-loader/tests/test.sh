#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
flags=(-std=c17 -Wall -Wextra -Wpedantic -g)

"$cc" "${flags[@]}" -c "$ROOT/examples/provider.c" -o "$ROOT/build/provider.o"
"$cc" "${flags[@]}" -c "$ROOT/examples/main_ref.c" -o "$ROOT/build/main_ref.o"
nm -u "$ROOT/build/main_ref.o" | grep -q 'provided_value'
"$cc" "$ROOT/build/main_ref.o" "$ROOT/build/provider.o" -o "$ROOT/build/resolved"
test "$("$ROOT/build/resolved")" = '42'

"$cc" "${flags[@]}" "$ROOT/examples/weak_demo.c" "$ROOT/examples/strong_override.c" -o "$ROOT/build/weak-strong"
test "$("$ROOT/build/weak-strong")" = '99'

"$cc" "${flags[@]}" "$ROOT/examples/constructor.c" -o "$ROOT/build/constructor"
test "$("$ROOT/build/constructor")" = $'constructor\nmain'

make -C "$ROOT/projects/static-demo" clean test CC="$cc"
make -C "$ROOT/projects/shared-demo" clean test CC="$cc"
make -C "$ROOT/projects/reloc-model" clean test CC="$cc"
readelf -d "$ROOT/projects/shared-demo/app" | grep -q 'NEEDED'
echo '[OK] chapter 07 linker/loader examples/projects'

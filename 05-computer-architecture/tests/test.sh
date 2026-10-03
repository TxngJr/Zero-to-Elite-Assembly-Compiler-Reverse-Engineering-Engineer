#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
flags=(-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g)
for src in "$ROOT"/examples/*.c; do name=$(basename "${src%.c}"); "$cc" "${flags[@]}" "$src" -o "$ROOT/build/$name"; "$ROOT/build/$name" >/dev/null; done
for p in tiny-cpu cache-sim branch-predictor; do make -C "$ROOT/projects/$p" clean test CC="$cc"; done
echo '[OK] chapter 05 architecture examples/projects'

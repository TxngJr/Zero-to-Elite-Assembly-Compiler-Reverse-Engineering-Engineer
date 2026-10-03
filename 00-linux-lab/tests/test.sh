#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
flags=(-std=c17 -Wall -Wextra -Wpedantic -g)
"$cc" "${flags[@]}" "$ROOT/examples/hello.c" -o "$ROOT/build/hello"
"$cc" "${flags[@]}" "$ROOT/examples/streams.c" -o "$ROOT/build/streams"
"$cc" "${flags[@]}" "$ROOT/examples/debug_me.c" -o "$ROOT/build/debug_me"
[[ "$("$ROOT/build/hello")" == 'Hello, systems world!' ]]
[[ "$("$ROOT/build/debug_me")" == 'answer=42' ]]
file "$ROOT/build/hello" | grep -qiE 'ELF|executable'
echo '[OK] chapter 00 examples compile and run'

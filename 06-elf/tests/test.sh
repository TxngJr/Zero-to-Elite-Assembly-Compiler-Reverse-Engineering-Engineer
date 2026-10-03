#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
flags=(-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g)
"$cc" "${flags[@]}" "$ROOT/examples/hello.c" -o "$ROOT/build/hello"
"$cc" "${flags[@]}" -no-pie "$ROOT/examples/hello.c" -o "$ROOT/build/hello-nopie"
"$cc" "${flags[@]}" "$ROOT/examples/sections.c" -o "$ROOT/build/sections"
"$cc" "${flags[@]}" "$ROOT/examples/custom_section.c" -o "$ROOT/build/custom-section"
"$cc" "${flags[@]}" -c "$ROOT/examples/reloc_user.c" -o "$ROOT/build/reloc_user.o"
"$cc" "${flags[@]}" -c "$ROOT/examples/reloc_def.c" -o "$ROOT/build/reloc_def.o"
readelf -h "$ROOT/build/hello" | grep -q 'ELF64'
readelf -S "$ROOT/build/sections" | grep -q '\.bss'
readelf -S "$ROOT/build/custom-section" | grep -q '\.course_meta'
readelf -r "$ROOT/build/reloc_user.o" | grep -q 'Relocation section'
nm -u "$ROOT/build/reloc_user.o" | grep -q 'plus_one'
make -C "$ROOT/projects/elf-inspector" clean test CC="$cc"
echo '[OK] chapter 06 ELF examples/projects'

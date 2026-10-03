#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT/build"
cc=${CC:-gcc}
flags=(-std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -g)
"$cc" "${flags[@]}" "$ROOT/examples/abi_args.s" "$ROOT/examples/abi_args_test.c" -o "$ROOT/build/abi-args"
"$ROOT/build/abi-args"
"$cc" "${flags[@]}" "$ROOT/examples/callee_saved.s" "$ROOT/examples/callee_saved_test.c" -o "$ROOT/build/callee-saved"
"$ROOT/build/callee-saved"
"$cc" -nostdlib -static -Wl,--build-id=none "$ROOT/examples/syscall_hello.s" -o "$ROOT/build/syscall-hello"
[[ "$("$ROOT/build/syscall-hello")" == 'hello via Linux syscall' ]]
make -C "$ROOT/projects/abi-lab" clean test CC="$cc"
make -C "$ROOT/projects/syscall-cat" clean test CC="$cc"
echo '[OK] chapter 04 ABI/syscall examples/projects'

#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CC=${CC:-gcc}
LD=${LD:-ld}

make -C "$ROOT" kernel CC="$CC" LD="$LD" >/dev/null
KERNEL="$ROOT/build/kernel.elf"

file "$KERNEL" > "$ROOT/build/file.txt"
grep -qi 'ELF 64-bit' "$ROOT/build/file.txt"

readelf -h "$KERNEL" > "$ROOT/build/elf-header.txt"
grep -q 'Advanced Micro Devices X86-64' "$ROOT/build/elf-header.txt"

readelf -S "$KERNEL" > "$ROOT/build/sections.txt"
grep -q '\.multiboot' "$ROOT/build/sections.txt"
grep -q '\.text' "$ROOT/build/sections.txt"
grep -q '\.bss' "$ROOT/build/sections.txt"

python3 "$ROOT/tests/check_multiboot.py" "$KERNEL"

nm "$KERNEL" > "$ROOT/build/kernel.nm"
grep -q ' T _start$' "$ROOT/build/kernel.nm"
grep -q ' T kernel_main$' "$ROOT/build/kernel.nm"
grep -q ' T exception_panic$' "$ROOT/build/kernel.nm"
grep -q ' T exception_pf_stub$' "$ROOT/build/kernel.nm"
grep -q ' T irq0_stub$' "$ROOT/build/kernel.nm"
grep -q ' T pmm_alloc_frame$' "$ROOT/build/kernel.nm"
grep -q ' T shell_feed_char$' "$ROOT/build/kernel.nm"
grep -q ' T shell_feed_scancode$' "$ROOT/build/kernel.nm"

objdump -d -Mintel "$KERNEL" > "$ROOT/build/kernel.dis"
grep -q 'wrmsr' "$ROOT/build/kernel.dis"
grep -q 'lidt' "$ROOT/build/kernel.dis"
grep -q 'iretq' "$ROOT/build/kernel.dis"
grep -q 'mov.*cr2' "$ROOT/build/kernel.dis"

grep -q 'console_try_read' "$ROOT/kernel/console.c"
grep -q 'shell_feed_char' "$ROOT/kernel/kernel.c"

echo '[OK] chapter 14 kernel image static checks'

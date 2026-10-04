#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

GRUB_MKRESCUE=$(command -v grub2-mkrescue 2>/dev/null || command -v grub-mkrescue 2>/dev/null || true)

for tool in xorriso qemu-system-x86_64 python3; do
  command -v "$tool" >/dev/null 2>&1 || {
    echo "[ERROR] missing required boot-test tool: $tool" >&2
    exit 2
  }
done

if [[ -z "$GRUB_MKRESCUE" ]]; then
  echo '[ERROR] missing grub2-mkrescue/grub-mkrescue' >&2
  exit 2
fi

make -C "$ROOT" iso GRUB_MKRESCUE="$GRUB_MKRESCUE"
rm -f "$ROOT/build/serial.log"

python3 "$ROOT/tests/qemu_interactive.py"   "$ROOT/build/eliteos.iso"   "$ROOT/build/serial.log"

grep -q 'EliteOS64 booted' "$ROOT/build/serial.log"
grep -q '\[BOOT\] pit irq ok' "$ROOT/build/serial.log"
grep -q '\[BOOT\] shell ready (serial + ps2 input)' "$ROOT/build/serial.log"
grep -q 'ticks=' "$ROOT/build/serial.log"

echo '[OK] QEMU runtime gate proved boot + PIT + serial shell input/output'

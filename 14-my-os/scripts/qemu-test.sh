#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

GRUB_MKRESCUE=$(command -v grub2-mkrescue 2>/dev/null || command -v grub-mkrescue 2>/dev/null || true)

for tool in xorriso qemu-system-x86_64 timeout; do
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

set +e
timeout 8s qemu-system-x86_64 \
  -accel tcg \
  -m 128M \
  -cdrom "$ROOT/build/eliteos.iso" \
  -serial "file:$ROOT/build/serial.log" \
  -display none \
  -no-reboot \
  -no-shutdown
status=$?
set -e

if [[ "$status" -ne 0 && "$status" -ne 124 ]]; then
  echo "[ERROR] QEMU exited unexpectedly with status $status" >&2
  exit 1
fi

grep -q 'EliteOS64 booted' "$ROOT/build/serial.log"
grep -q '\[BOOT\] console ok' "$ROOT/build/serial.log"
grep -q '\[BOOT\] pmm/heap ok' "$ROOT/build/serial.log"
grep -q '\[BOOT\] idt/pic/pit configured' "$ROOT/build/serial.log"
grep -q '\[BOOT\] pit irq ok' "$ROOT/build/serial.log"
grep -q '\[BOOT\] shell ready (serial + ps2 input)' "$ROOT/build/serial.log"
grep -q 'elite> ' "$ROOT/build/serial.log"

echo '[OK] QEMU boot reached interactive shell and PIT IRQs fired'

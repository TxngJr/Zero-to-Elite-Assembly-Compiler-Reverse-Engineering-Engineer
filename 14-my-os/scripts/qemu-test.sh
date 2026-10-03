#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

for tool in grub2-mkrescue xorriso qemu-system-x86_64 timeout; do
  command -v "$tool" >/dev/null 2>&1 || {
    echo "[ERROR] missing required boot-test tool: $tool" >&2
    exit 2
  }
done

make -C "$ROOT" iso
rm -f "$ROOT/build/serial.log"

set +e
timeout 8s qemu-system-x86_64   -accel tcg   -m 128M   -cdrom "$ROOT/build/eliteos.iso"   -serial "file:$ROOT/build/serial.log"   -display none   -no-reboot   -no-shutdown
status=$?
set -e

if [[ "$status" -ne 0 && "$status" -ne 124 ]]; then
  echo "[ERROR] QEMU exited unexpectedly with status $status" >&2
  exit 1
fi

grep -q 'EliteOS64 booted' "$ROOT/build/serial.log"
grep -q 'multiboot2 info=' "$ROOT/build/serial.log"
echo '[OK] QEMU boot reached EliteOS64 kernel_main'

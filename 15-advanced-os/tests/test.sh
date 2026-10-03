#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CC=${CC:-gcc}
PY=${PYTHON:-python3}

make -C "$ROOT/projects/scheduler-sim" clean test CC="$CC"
make -C "$ROOT/projects/vfs-sim" clean test CC="$CC"
make -C "$ROOT/projects/ipc-sim" clean test CC="$CC"
$PY "$ROOT/projects/vm-cow-sim/vm_cow.py" > "$ROOT/vm.out"
grep -q 'vm-cow-sim: OK' "$ROOT/vm.out"
$PY -m py_compile "$ROOT/projects/vm-cow-sim/vm_cow.py"
rm -f "$ROOT/vm.out"
echo '[OK] chapter 15 advanced OS simulators'

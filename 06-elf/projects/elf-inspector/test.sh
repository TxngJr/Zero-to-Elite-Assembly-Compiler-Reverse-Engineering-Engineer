#!/usr/bin/env bash
set -euo pipefail
./elf-inspector fixture > out.txt
grep -q '^ELF64 ' out.txt
grep -q 'LOAD' out.txt
grep -q '\.text' out.txt
printf 'not elf\n' > bad.bin
set +e
./elf-inspector bad.bin >/dev/null 2>&1
s=$?
set -e
test "$s" -ne 0
rm -f out.txt bad.bin
echo '[OK] elf-inspector tests'

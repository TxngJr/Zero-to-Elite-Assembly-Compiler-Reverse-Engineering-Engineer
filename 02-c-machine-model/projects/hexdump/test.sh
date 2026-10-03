#!/usr/bin/env bash
set -euo pipefail
printf 'ABC\n' > sample.bin
./zs-hexdump sample.bin > out.txt
grep -q '41 42 43 0a' out.txt
grep -q '|ABC\.' out.txt
: > empty.bin
[[ "$(./zs-hexdump empty.bin)" == '00000000' ]]
rm -f sample.bin empty.bin out.txt
echo '[OK] hexdump tests'

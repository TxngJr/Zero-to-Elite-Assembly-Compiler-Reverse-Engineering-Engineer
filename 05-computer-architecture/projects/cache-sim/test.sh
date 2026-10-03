#!/usr/bin/env bash
set -euo pipefail
printf '0\n4\n0\n8\n0\n' | ./cache-sim 2 4 > out.txt
grep -q 'hits=1 misses=4' out.txt
rm -f out.txt
echo '[OK] cache-sim tests'

#!/usr/bin/env bash
set -u
ok=0; missing=0; optional_ok=0; optional_missing=0
print_tool() {
  local label=$1 cmd=$2 flag=${3:---version}
  if command -v "$cmd" >/dev/null 2>&1; then
    local first
    first=$("$cmd" "$flag" 2>&1 | head -n1)
    printf '[OK] %-12s %s\n' "$label" "$first"
    ok=$((ok+1))
  else
    printf '[MISSING] %-12s %s\n' "$label" "$cmd"
    missing=$((missing+1))
  fi
}
print_optional() {
  local label=$1 cmd=$2
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '[OPTIONAL] %-12s installed\n' "$label"
    optional_ok=$((optional_ok+1))
  else
    printf '[OPTIONAL] %-12s missing\n' "$label"
    optional_missing=$((optional_missing+1))
  fi
}
echo '=== System ==='
if [[ -r /etc/os-release ]]; then . /etc/os-release; echo "Distribution : ${PRETTY_NAME:-unknown}"; fi
echo "Kernel       : $(uname -sr)"
echo "Architecture : $(uname -m)"
if command -v lscpu >/dev/null 2>&1; then
  echo "CPU model    : $(lscpu | awk -F: '/Model name/{sub(/^[ \t]+/,"",$2); print $2; exit}')"
  echo "CPU(s)       : $(lscpu | awk -F: '/^CPU\(s\):/{sub(/^[ \t]+/,"",$2); print $2; exit}')"
fi
if command -v free >/dev/null 2>&1; then echo "RAM          : $(free -h | awk '/^Mem:/{print $2}')"; fi
echo; echo '=== Required tools ==='
print_tool gcc gcc
print_tool clang clang
print_tool ld ld
print_tool as as
print_tool objdump objdump
print_tool readelf readelf
print_tool nm nm
print_tool ar ar
print_tool gdb gdb
print_tool make make
print_tool cmake cmake
print_tool python python3
print_tool git git
print_tool file file --version
print_tool strace strace --version
echo; echo '=== Optional tools ==='
print_optional nasm nasm
print_optional ltrace ltrace
print_optional rg rg
print_optional fd fdfind
print_optional perf perf
print_optional eu-readelf eu-readelf
print_optional valgrind valgrind
echo; echo '=== Summary ==='
echo "Required tools: $ok present, $missing missing"
echo "Optional tools: $optional_ok present, $optional_missing missing"
if (( missing == 0 )); then
  echo 'Ready for Chapters 00–08.'
  exit 0
else
  echo 'Install missing required tools before continuing.'
  exit 1
fi

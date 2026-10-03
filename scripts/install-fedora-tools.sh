#!/usr/bin/env bash
set -euo pipefail

if ! command -v dnf >/dev/null 2>&1; then
  echo "[ERROR] This installer targets Fedora systems with dnf." >&2
  exit 1
fi

required=(
  gcc gcc-c++ clang llvm lld binutils gdb make cmake ninja-build
  git python3 python3-pip strace ltrace file which tree ripgrep
  fd-find pkgconf glibc-devel libstdc++-devel
)

optional=(
  nasm glibc-static perf elfutils valgrind
  qemu-system-x86-core grub2-tools-extra grub2-pc-modules xorriso
)

echo "Required packages: ${required[*]}"
echo "Optional packages: ${optional[*]}"

sudo dnf install -y "${required[@]}"

for pkg in "${optional[@]}"; do
  if dnf -q list --available "$pkg" >/dev/null 2>&1 || rpm -q "$pkg" >/dev/null 2>&1; then
    sudo dnf install -y "$pkg" || echo "[OPTIONAL] Could not install $pkg"
  else
    echo "[OPTIONAL] $pkg is not available from enabled repositories"
  fi
done

echo "Tool installation step completed. Run ./scripts/check-environment.sh next."

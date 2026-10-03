#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
import subprocess

FUNC_RE = re.compile(r"^([0-9a-f]+) <([^>]+)>:$")
INSN_RE = re.compile(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*([^\s]+)\s*(.*)$")
TARGET_RE = re.compile(r"([0-9a-f]+)\s*<([^>]+)>")

def main() -> int:
    ap = argparse.ArgumentParser(description="Simple CFG edge summary for course binaries")
    ap.add_argument("binary")
    args = ap.parse_args()

    text = subprocess.check_output(["objdump", "-d", "-Mintel", args.binary], text=True)
    current = None
    edges: list[tuple[str, str, str]] = []

    for line in text.splitlines():
        fm = FUNC_RE.match(line.strip())
        if fm:
            current = fm.group(2)
            continue

        im = INSN_RE.match(line)
        if not im or current is None:
            continue

        mnemonic = im.group(2)
        operands = im.group(3)
        if mnemonic.startswith("j") or mnemonic.startswith("call"):
            tm = TARGET_RE.search(operands)
            if tm:
                edges.append((current, mnemonic, tm.group(2)))

    for src, kind, dst in edges:
        print(f"{src} --{kind}--> {dst}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

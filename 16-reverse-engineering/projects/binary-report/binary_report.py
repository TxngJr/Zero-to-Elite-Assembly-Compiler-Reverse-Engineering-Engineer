#!/usr/bin/env python3
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

def run(*args: str) -> str:
    proc = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.stdout

def main() -> int:
    ap = argparse.ArgumentParser(description="Static report for authorized/course binaries")
    ap.add_argument("binary")
    args = ap.parse_args()

    path = Path(args.binary)
    data = path.read_bytes()
    report = {
        "path": str(path),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "file": run("file", str(path)).strip(),
        "elf_header": run("readelf", "-hW", str(path)),
        "program_headers": run("readelf", "-lW", str(path)),
        "sections": run("readelf", "-SW", str(path)),
        "dynamic": run("readelf", "-dW", str(path)),
        "symbols": run("nm", "-an", str(path)),
        "strings": run("strings", "-a", str(path)),
    }
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

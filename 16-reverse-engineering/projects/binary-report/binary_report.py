#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

class ReportError(RuntimeError):
    pass

def run_required(*args: str) -> str:
    try:
        proc = subprocess.run(
            args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as exc:
        raise ReportError(f"cannot run {args[0]}: {exc}") from exc

    if proc.returncode != 0:
        raise ReportError(
            f"{' '.join(args)} failed with status {proc.returncode}:\n{proc.stdout}"
        )
    return proc.stdout

def run_optional(*args: str) -> dict[str, object]:
    try:
        proc = subprocess.run(
            args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as exc:
        return {
            "status": "unavailable",
            "returncode": None,
            "output": str(exc),
        }

    return {
        "status": "ok" if proc.returncode == 0 else "nonzero",
        "returncode": proc.returncode,
        "output": proc.stdout,
    }

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Static report for authorized/course ELF binaries"
    )
    parser.add_argument("binary")
    args = parser.parse_args()

    path = Path(args.binary)
    try:
        data = path.read_bytes()

        # These are required for an ELF report. A failure makes the report fail.
        file_output = run_required("file", str(path)).strip()
        elf_header = run_required("readelf", "-hW", str(path))
        program_headers = run_required("readelf", "-lW", str(path))
        sections = run_required("readelf", "-SW", str(path))
        dynamic = run_required("readelf", "-dW", str(path))

        report = {
            "path": str(path),
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "file": file_output,
            "elf_header": elf_header,
            "program_headers": program_headers,
            "sections": sections,
            "dynamic": dynamic,
            # nm may legitimately return non-zero for a fully stripped file.
            "symbols": run_optional("nm", "-an", str(path)),
            "strings": run_optional("strings", "-a", str(path)),
        }

        print(json.dumps(report, indent=2))
        return 0

    except (OSError, ReportError) as exc:
        print(f"binary-report: error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

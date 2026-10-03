#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path

ERROR_RE = re.compile(r"ERROR: AddressSanitizer: ([^\s]+)")
FRAME_RE = re.compile(r"^\s*#\d+\s+0x[0-9a-fA-F]+\s+in\s+(.+)$")

def main() -> int:
    ap = argparse.ArgumentParser(description="Small sanitizer-log summarizer for course labs")
    ap.add_argument("log")
    args = ap.parse_args()

    text = Path(args.log).read_text(encoding="utf-8", errors="replace")
    error = ERROR_RE.search(text)
    frames = []

    for line in text.splitlines():
        m = FRAME_RE.match(line)
        if m:
            frames.append(m.group(1))

    print("sanitizer_error=" + (error.group(1) if error else "unknown"))
    if frames:
        print("first_frame=" + frames[0])
    print(f"frames={len(frames)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

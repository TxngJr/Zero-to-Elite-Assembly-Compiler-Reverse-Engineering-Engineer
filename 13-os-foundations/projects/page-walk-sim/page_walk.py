#!/usr/bin/env python3
from __future__ import annotations
import argparse

PAGE = 4096
MASK64 = (1 << 64) - 1

def canonical(va: int) -> bool:
    if va < 0 or va > MASK64:
        return False
    sign = (va >> 47) & 1
    high = va >> 48
    return high == (0xFFFF if sign else 0)

def split_va(va: int):
    if not canonical(va):
        raise ValueError("non-canonical x86-64 address")
    return {
        "pml4": (va >> 39) & 0x1FF,
        "pdpt": (va >> 30) & 0x1FF,
        "pd": (va >> 21) & 0x1FF,
        "pt": (va >> 12) & 0x1FF,
        "offset": va & 0xFFF,
    }

class PageTableSim:
    def __init__(self):
        self.pages = {}

    def map_page(self, va: int, pa: int, flags: str = "rw"):
        if va % PAGE or pa % PAGE:
            raise ValueError("page alignment required")
        if not canonical(va):
            raise ValueError("non-canonical virtual address")
        self.pages[va // PAGE] = (pa // PAGE, flags)

    def translate(self, va: int, *, write=False, execute=False) -> int:
        if not canonical(va):
            raise ValueError("non-canonical virtual address")
        vpn = va // PAGE
        if vpn not in self.pages:
            raise KeyError("page not present")
        ppn, flags = self.pages[vpn]
        if write and "w" not in flags:
            raise PermissionError("write denied")
        if execute and "x" not in flags:
            raise PermissionError("execute denied")
        return ppn * PAGE + (va % PAGE)

def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("split")
    p.add_argument("va", type=lambda s: int(s, 0))
    sub.add_parser("demo")
    args = ap.parse_args()

    if args.cmd == "split":
        try:
            fields = split_va(args.va)
        except ValueError as exc:
            print(f"error: {exc}")
            return 1
        print(" ".join(f"{k}={v}" for k, v in fields.items()))
        return 0

    sim = PageTableSim()
    sim.map_page(0x400000, 0x200000, "rwx")
    sim.map_page(0x401000, 0x900000, "rw")
    print(hex(sim.translate(0x400123, execute=True)))
    print(hex(sim.translate(0x401456, write=True)))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

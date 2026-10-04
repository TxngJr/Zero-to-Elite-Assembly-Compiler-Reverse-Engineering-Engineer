#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import argparse
import json

@dataclass(frozen=True)
class Interval:
    name: str
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError(f"invalid interval {self.name}: {self.start}..{self.end}")

@dataclass
class Allocation:
    location: str
    spilled: bool

def linear_scan_allocate(
    intervals: list[Interval],
    registers: list[str],
) -> dict[str, Allocation]:
    if not registers:
        raise ValueError("at least one register is required")

    ordered = sorted(intervals, key=lambda item: (item.start, item.end, item.name))
    active: list[tuple[Interval, str]] = []
    free = list(registers)
    result: dict[str, Allocation] = {}
    next_spill = 0

    def expire(before_start: int) -> None:
        nonlocal active, free
        keep: list[tuple[Interval, str]] = []
        for interval, reg in active:
            if interval.end < before_start:
                free.append(reg)
            else:
                keep.append((interval, reg))
        active = sorted(keep, key=lambda item: item[0].end)
        free.sort(key=registers.index)

    def new_spill_slot() -> str:
        nonlocal next_spill
        slot = f"spill[{next_spill}]"
        next_spill += 1
        return slot

    for current in ordered:
        if current.name in result:
            raise ValueError(f"duplicate interval name: {current.name}")

        expire(current.start)

        if free:
            reg = free.pop(0)
            result[current.name] = Allocation(reg, False)
            active.append((current, reg))
            active.sort(key=lambda item: item[0].end)
            continue

        spill_interval, spill_reg = max(
            active,
            key=lambda item: (item[0].end, item[0].start, item[0].name),
        )

        if spill_interval.end > current.end:
            result[spill_interval.name] = Allocation(new_spill_slot(), True)
            active.remove((spill_interval, spill_reg))
            result[current.name] = Allocation(spill_reg, False)
            active.append((current, spill_reg))
            active.sort(key=lambda item: item[0].end)
        else:
            result[current.name] = Allocation(new_spill_slot(), True)

    return result

def demo() -> tuple[list[Interval], list[str]]:
    return (
        [
            Interval("a", 0, 8),
            Interval("b", 1, 3),
            Interval("c", 2, 6),
            Interval("d", 4, 5),
            Interval("e", 7, 10),
        ],
        ["r10", "r11"],
    )

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Educational linear-scan register allocator"
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    intervals, registers = demo()
    allocation = linear_scan_allocate(intervals, registers)

    if args.json:
        print(
            json.dumps(
                {
                    name: {
                        "location": item.location,
                        "spilled": item.spilled,
                    }
                    for name, item in sorted(allocation.items())
                },
                indent=2,
            )
        )
    else:
        for interval in intervals:
            item = allocation[interval.name]
            print(
                f"{interval.name:>4} {interval.start:>2}..{interval.end:<2} "
                f"-> {item.location}"
            )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

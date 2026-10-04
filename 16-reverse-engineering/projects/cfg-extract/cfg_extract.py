#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import re
import subprocess
import sys

FUNC_RE = re.compile(r"^([0-9a-f]+) <([^>]+)>:$")
INSN_RE = re.compile(
    r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*([^\s]+)\s*(.*)$"
)
TARGET_RE = re.compile(r"^\s*([0-9a-f]+)(?:\s*<([^>]+)>)?")

CONDITIONAL_PREFIXES = (
    "ja", "jb", "jc", "je", "jg", "jl", "jn", "jo", "jp", "js", "jz"
)

@dataclass
class Instruction:
    address: int
    mnemonic: str
    operands: str

@dataclass
class Function:
    name: str
    address: int
    instructions: list[Instruction]

def parse_objdump(text: str) -> list[Function]:
    functions: list[Function] = []
    current: Function | None = None

    for line in text.splitlines():
        fm = FUNC_RE.match(line.strip())
        if fm:
            current = Function(fm.group(2), int(fm.group(1), 16), [])
            functions.append(current)
            continue

        im = INSN_RE.match(line)
        if im and current is not None:
            current.instructions.append(
                Instruction(
                    int(im.group(1), 16),
                    im.group(2).lower(),
                    im.group(3).strip(),
                )
            )

    return functions

def direct_target(insn: Instruction) -> tuple[int, str | None] | None:
    match = TARGET_RE.match(insn.operands)
    if not match:
        return None
    return int(match.group(1), 16), match.group(2)

def is_conditional_jump(mnemonic: str) -> bool:
    return mnemonic.startswith(CONDITIONAL_PREFIXES) and mnemonic != "jmp"

def is_return(mnemonic: str) -> bool:
    return mnemonic.startswith("ret")

def analyze_function(fn: Function) -> dict[str, object]:
    if not fn.instructions:
        return {
            "name": fn.name,
            "address": fn.address,
            "blocks": [],
            "calls": [],
        }

    addresses = [insn.address for insn in fn.instructions]
    address_set = set(addresses)
    next_address: dict[int, int | None] = {}
    for index, address in enumerate(addresses):
        next_address[address] = (
            addresses[index + 1] if index + 1 < len(addresses) else None
        )

    leaders = {addresses[0]}
    calls: list[dict[str, object]] = []

    for insn in fn.instructions:
        target = direct_target(insn)

        if insn.mnemonic.startswith("call"):
            if target:
                calls.append(
                    {
                        "site": insn.address,
                        "target": target[0],
                        "target_name": target[1],
                    }
                )
            continue

        if insn.mnemonic == "jmp" or is_conditional_jump(insn.mnemonic):
            if target and target[0] in address_set:
                leaders.add(target[0])
            fallthrough = next_address[insn.address]
            if is_conditional_jump(insn.mnemonic) and fallthrough is not None:
                leaders.add(fallthrough)
            elif insn.mnemonic == "jmp" and fallthrough is not None:
                # The next bytes can start an unreachable/referenced block.
                leaders.add(fallthrough)
        elif is_return(insn.mnemonic):
            fallthrough = next_address[insn.address]
            if fallthrough is not None:
                leaders.add(fallthrough)

    ordered_leaders = sorted(leaders)
    block_for: dict[int, int] = {}
    blocks: list[dict[str, object]] = []

    leader_index = 0
    current_leader = ordered_leaders[0]
    current_instructions: list[Instruction] = []

    def finish_block() -> None:
        if not current_instructions:
            return
        blocks.append(
            {
                "start": current_leader,
                "end": current_instructions[-1].address,
                "instructions": [insn.address for insn in current_instructions],
                "edges": [],
            }
        )
        for insn in current_instructions:
            block_for[insn.address] = current_leader

    for insn in fn.instructions:
        if (
            insn.address in leaders
            and insn.address != current_leader
            and current_instructions
        ):
            finish_block()
            leader_index += 1
            current_leader = ordered_leaders[leader_index]
            current_instructions = []
        current_instructions.append(insn)

    finish_block()
    block_by_start = {block["start"]: block for block in blocks}

    for block in blocks:
        last_addr = block["end"]
        last = next(insn for insn in fn.instructions if insn.address == last_addr)
        target = direct_target(last)

        def add_edge(kind: str, target_addr: int | None) -> None:
            if target_addr is None:
                return
            if target_addr not in block_by_start:
                return
            block["edges"].append({"kind": kind, "target": target_addr})

        if last.mnemonic == "jmp":
            add_edge("branch", target[0] if target else None)
        elif is_conditional_jump(last.mnemonic):
            add_edge("branch", target[0] if target else None)
            add_edge("fallthrough", next_address[last.address])
        elif not is_return(last.mnemonic):
            add_edge("fallthrough", next_address[last.address])

    return {
        "name": fn.name,
        "address": fn.address,
        "blocks": blocks,
        "calls": calls,
    }

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Basic-block CFG summary for authorized/course binaries"
    )
    parser.add_argument("binary")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        text = subprocess.check_output(
            ["objdump", "-d", "-Mintel", args.binary],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"cfg-extract: error: {exc}", file=sys.stderr)
        return 1

    analysis = [analyze_function(fn) for fn in parse_objdump(text)]

    if args.json:
        print(json.dumps(analysis, indent=2))
        return 0

    for fn in analysis:
        print(f"function {fn['name']} @ 0x{fn['address']:x}")
        for block in fn["blocks"]:
            print(f"  block 0x{block['start']:x}..0x{block['end']:x}")
            for edge in block["edges"]:
                print(
                    f"    --{edge['kind']}--> 0x{edge['target']:x}"
                )
        for call in fn["calls"]:
            target_name = call["target_name"] or f"0x{call['target']:x}"
            print(
                f"  0x{call['site']:x} --call--> {target_name}"
            )

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

@dataclass
class SSAInstruction:
    op: str
    dst: str | None
    args: list[str]

@dataclass
class SSABlock:
    label: str
    phis: list[tuple[str, str, dict[str, str]]] = field(default_factory=list)
    instrs: list[SSAInstruction] = field(default_factory=list)
    term: SSAInstruction | None = None

@dataclass
class SSAFunction:
    name: str
    params: list[str]
    blocks: list[SSABlock]

def _successors(fn: Any) -> dict[str, list[str]]:
    result = {block.label: [] for block in fn.blocks}
    for block in fn.blocks:
        term = block.term
        if term is None:
            continue
        if term.op == "jump":
            result[block.label] = [term.args[0]]
        elif term.op == "cjump":
            result[block.label] = list(term.args[1:3])
    return result

def _predecessors(fn: Any) -> dict[str, list[str]]:
    result = {block.label: [] for block in fn.blocks}
    for src, targets in _successors(fn).items():
        for dst in targets:
            if dst not in result:
                raise ValueError(f"unknown CFG target {dst!r} from {src!r}")
            result[dst].append(src)
    return result

def _dominators(fn: Any) -> dict[str, set[str]]:
    labels = [block.label for block in fn.blocks]
    if not labels:
        return {}
    preds = _predecessors(fn)
    entry = labels[0]
    dom = {label: set(labels) for label in labels}
    dom[entry] = {entry}

    changed = True
    while changed:
        changed = False
        for label in labels[1:]:
            incoming = preds[label]
            common = (
                set.intersection(*(dom[pred] for pred in incoming))
                if incoming
                else set()
            )
            new = {label} | common
            if new != dom[label]:
                dom[label] = new
                changed = True
    return dom

def immediate_dominators(fn: Any) -> dict[str, str | None]:
    dom = _dominators(fn)
    labels = [block.label for block in fn.blocks]
    if not labels:
        return {}

    entry = labels[0]
    result: dict[str, str | None] = {entry: None}
    for label in labels[1:]:
        strict = dom[label] - {label}
        if not strict:
            result[label] = None
            continue
        result[label] = max(strict, key=lambda candidate: len(dom[candidate]))
    return result

def dominance_frontiers(fn: Any) -> dict[str, set[str]]:
    labels = [block.label for block in fn.blocks]
    preds = _predecessors(fn)
    idom = immediate_dominators(fn)
    frontiers = {label: set() for label in labels}

    for block in labels:
        if len(preds[block]) < 2:
            continue
        stop = idom[block]
        for pred in preds[block]:
            runner: str | None = pred
            while runner is not None and runner != stop:
                frontiers[runner].add(block)
                runner = idom[runner]
    return frontiers

def _source_name(name: str | None) -> bool:
    return bool(name) and not name.startswith("%") and name.isidentifier()

def _definition_blocks(fn: Any) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    entry = fn.blocks[0].label
    for param in fn.params:
        result[param].add(entry)
    for block in fn.blocks:
        for ins in block.instrs:
            if _source_name(ins.dst):
                result[ins.dst].add(block.label)
    return result

def place_phi_nodes(fn: Any) -> dict[str, set[str]]:
    frontiers = dominance_frontiers(fn)
    defs = _definition_blocks(fn)
    phis: dict[str, set[str]] = {block.label: set() for block in fn.blocks}

    for variable, defsites in defs.items():
        work = list(defsites)
        placed: set[str] = set()

        while work:
            block = work.pop()
            for frontier in frontiers[block]:
                if frontier in placed:
                    continue
                phis[frontier].add(variable)
                placed.add(frontier)
                if frontier not in defsites:
                    work.append(frontier)

    return phis

def _rename_instruction_args(
    op: str,
    args: list[str],
    current,
) -> list[str]:
    if op == "const":
        return list(args)
    if op == "mov":
        return [current(args[0])]
    if op == "un":
        return [args[0], current(args[1])]
    if op in ("bin", "cmp"):
        return [args[0], current(args[1]), current(args[2])]
    if op == "call":
        return [args[0], *[current(arg) for arg in args[1:]]]
    return [current(arg) if _source_name(arg) else arg for arg in args]

def construct_ssa(fn: Any) -> SSAFunction:
    if not fn.blocks:
        return SSAFunction(fn.name, list(fn.params), [])

    labels = [block.label for block in fn.blocks]
    block_map = {block.label: block for block in fn.blocks}
    succ = _successors(fn)
    preds = _predecessors(fn)
    idom = immediate_dominators(fn)
    phi_vars = place_phi_nodes(fn)

    dom_children: dict[str, list[str]] = {label: [] for label in labels}
    for label, parent in idom.items():
        if parent is not None:
            dom_children[parent].append(label)
    for children in dom_children.values():
        children.sort()

    counters: dict[str, int] = defaultdict(lambda: -1)
    stacks: dict[str, list[str]] = defaultdict(list)
    phi_dest: dict[str, dict[str, str]] = {label: {} for label in labels}
    phi_inputs: dict[str, dict[str, dict[str, str]]] = {
        label: {var: {} for var in phi_vars[label]} for label in labels
    }
    renamed: dict[str, SSABlock] = {
        label: SSABlock(label) for label in labels
    }

    def fresh(variable: str) -> str:
        counters[variable] += 1
        return f"{variable}.{counters[variable]}"

    versioned_params: list[str] = []
    for param in fn.params:
        name = fresh(param)
        stacks[param].append(name)
        versioned_params.append(name)

    def current(value: str) -> str:
        if _source_name(value) and stacks[value]:
            return stacks[value][-1]
        return value

    def visit(label: str) -> None:
        source = block_map[label]
        target = renamed[label]
        pushed: list[str] = []

        for variable in sorted(phi_vars[label]):
            name = fresh(variable)
            stacks[variable].append(name)
            pushed.append(variable)
            phi_dest[label][variable] = name

        for ins in source.instrs:
            args = _rename_instruction_args(ins.op, list(ins.args), current)
            dst = ins.dst
            if _source_name(dst):
                assert dst is not None
                new_dst = fresh(dst)
                stacks[dst].append(new_dst)
                pushed.append(dst)
                dst = new_dst
            target.instrs.append(SSAInstruction(ins.op, dst, args))

        if source.term is not None:
            term_args = list(source.term.args)
            if source.term.op in ("ret", "cjump") and term_args:
                term_args[0] = current(term_args[0])
            target.term = SSAInstruction(source.term.op, None, term_args)

        for successor in succ[label]:
            for variable in phi_vars[successor]:
                incoming = current(variable)
                if incoming == variable:
                    incoming = "undef"
                phi_inputs[successor][variable][label] = incoming

        for child in dom_children[label]:
            visit(child)

        for variable in reversed(pushed):
            stacks[variable].pop()

    visit(labels[0])

    for label in labels:
        target = renamed[label]
        for variable in sorted(phi_vars[label]):
            incoming = {
                pred: phi_inputs[label][variable].get(pred, "undef")
                for pred in preds[label]
            }
            target.phis.append(
                (variable, phi_dest[label][variable], incoming)
            )

    return SSAFunction(fn.name, versioned_params, [renamed[label] for label in labels])

def format_ssa(fn: Any) -> str:
    ssa = construct_ssa(fn)
    out = [f"fn {ssa.name}({', '.join(ssa.params)})"]

    for block in ssa.blocks:
        out.append(f"{block.label}:")
        for _variable, dst, incoming in block.phis:
            edges = " ".join(
                f"[{pred}: {value}]" for pred, value in incoming.items()
            )
            out.append(f"  {dst} = phi {edges}")

        for ins in block.instrs:
            lhs = f"{ins.dst} = " if ins.dst else ""
            out.append(f"  {lhs}{ins.op} {' '.join(ins.args)}".rstrip())

        if block.term is not None:
            out.append(
                f"  {block.term.op} {' '.join(block.term.args)}".rstrip()
            )

    return "\n".join(out)

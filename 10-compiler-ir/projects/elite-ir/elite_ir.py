#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import sys
from typing import Optional

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[3]
        / "09-compiler-frontend"
        / "projects"
        / "elite-frontend"
    ),
)
import elite_frontend as F

INT64_MIN = -(1 << 63)
INT64_MAX = (1 << 63) - 1
MASK64 = (1 << 64) - 1

class IRError(Exception):
    pass

@dataclass
class Instr:
    op: str
    dst: Optional[str] = None
    args: list[str] = field(default_factory=list)

@dataclass
class Block:
    label: str
    instrs: list[Instr] = field(default_factory=list)
    term: Optional[Instr] = None

@dataclass
class FunctionIR:
    name: str
    params: list[str]
    blocks: list[Block]

@dataclass
class ModuleIR:
    functions: list[FunctionIR]

def wrap_i64(value: int) -> int:
    value &= MASK64
    return value if value <= INT64_MAX else value - (1 << 64)

def trunc_div_i64(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError
    if a == INT64_MIN and b == -1:
        raise OverflowError("signed 64-bit division overflow")
    quotient = abs(a) // abs(b)
    return -quotient if (a < 0) != (b < 0) else quotient

def trunc_mod_i64(a: int, b: int) -> int:
    quotient = trunc_div_i64(a, b)
    return a - quotient * b

class Lowerer:
    def __init__(self) -> None:
        self.temp = 0
        self.label = 0
        self.blocks: list[Block] = []
        self.current: Optional[Block] = None

    def new_temp(self) -> str:
        self.temp += 1
        return f"%t{self.temp}"

    def new_label(self, prefix: str = "bb") -> str:
        self.label += 1
        return f"{prefix}{self.label}"

    def add_block(self, label: Optional[str] = None) -> Block:
        block = Block(label or self.new_label())
        self.blocks.append(block)
        self.current = block
        return block

    def emit(self, op: str, dst: Optional[str] = None, *args: str) -> Optional[str]:
        assert self.current is not None
        self.current.instrs.append(Instr(op, dst, list(args)))
        return dst

    def terminate(self, op: str, *args: str) -> None:
        assert self.current is not None
        self.current.term = Instr(op, None, list(args))

    def lower_module(self, program: F.Program) -> ModuleIR:
        return ModuleIR([self.lower_function(fn) for fn in program.functions])

    def lower_function(self, fn: F.Function) -> FunctionIR:
        self.temp = 0
        self.label = 0
        self.blocks = []
        self.add_block("entry")

        for statement in fn.body.statements:
            assert self.current is not None
            if self.current.term is None:
                self.lower_statement(statement)

        return FunctionIR(fn.name, [param.name for param in fn.params], self.blocks)

    def lower_statement(self, statement: F.Stmt) -> None:
        if isinstance(statement, F.Let):
            self.emit("mov", statement.name, self.lower_expression(statement.value))
            return

        if isinstance(statement, F.Assign):
            self.emit("mov", statement.name, self.lower_expression(statement.value))
            return

        if isinstance(statement, F.ExprStmt):
            self.lower_expression(statement.value)
            return

        if isinstance(statement, F.Return):
            self.terminate("ret", self.lower_expression(statement.value))
            return

        if isinstance(statement, F.If):
            condition = self.lower_expression(statement.cond)
            then_label = self.new_label("then")
            else_label = self.new_label("else")
            end_label = self.new_label("ifend")
            self.terminate("cjump", condition, then_label, else_label)

            self.add_block(then_label)
            for nested in statement.then_block.statements:
                assert self.current is not None
                if self.current.term is None:
                    self.lower_statement(nested)
            assert self.current is not None
            if self.current.term is None:
                self.terminate("jump", end_label)

            self.add_block(else_label)
            if statement.else_block:
                for nested in statement.else_block.statements:
                    assert self.current is not None
                    if self.current.term is None:
                        self.lower_statement(nested)
            assert self.current is not None
            if self.current.term is None:
                self.terminate("jump", end_label)

            self.add_block(end_label)
            return

        if isinstance(statement, F.While):
            cond_label = self.new_label("while_cond")
            body_label = self.new_label("while_body")
            end_label = self.new_label("while_end")

            self.terminate("jump", cond_label)
            self.add_block(cond_label)
            condition = self.lower_expression(statement.cond)
            self.terminate("cjump", condition, body_label, end_label)

            self.add_block(body_label)
            for nested in statement.body.statements:
                assert self.current is not None
                if self.current.term is None:
                    self.lower_statement(nested)
            assert self.current is not None
            if self.current.term is None:
                self.terminate("jump", cond_label)

            self.add_block(end_label)
            return

        raise IRError(f"unsupported statement {type(statement)}")

    def lower_expression(self, expr: F.Expr) -> str:
        if isinstance(expr, F.IntLit):
            temp = self.new_temp()
            self.emit("const", temp, str(expr.value))
            return temp

        if isinstance(expr, F.BoolLit):
            temp = self.new_temp()
            self.emit("const", temp, "1" if expr.value else "0")
            return temp

        if isinstance(expr, F.Var):
            return expr.name

        if isinstance(expr, F.Unary):
            arg = self.lower_expression(expr.expr)
            temp = self.new_temp()
            self.emit("un", temp, expr.op, arg)
            return temp

        if isinstance(expr, F.Call):
            args = [self.lower_expression(arg) for arg in expr.args]
            temp = self.new_temp()
            self.emit("call", temp, expr.name, *args)
            return temp

        if isinstance(expr, F.Binary) and expr.op in ("&&", "||"):
            result = self.new_temp()
            left = self.lower_expression(expr.left)
            rhs_label = self.new_label("logic_rhs")
            short_label = self.new_label("logic_short")
            done_label = self.new_label("logic_done")

            if expr.op == "&&":
                self.terminate("cjump", left, rhs_label, short_label)
            else:
                self.terminate("cjump", left, short_label, rhs_label)

            self.add_block(rhs_label)
            right = self.lower_expression(expr.right)
            self.emit("mov", result, right)
            self.terminate("jump", done_label)

            self.add_block(short_label)
            constant = self.new_temp()
            self.emit("const", constant, "0" if expr.op == "&&" else "1")
            self.emit("mov", result, constant)
            self.terminate("jump", done_label)

            self.add_block(done_label)
            return result

        if isinstance(expr, F.Binary):
            left = self.lower_expression(expr.left)
            right = self.lower_expression(expr.right)
            temp = self.new_temp()
            op = "cmp" if expr.op in ("<", "<=", ">", ">=", "==", "!=") else "bin"
            self.emit(op, temp, expr.op, left, right)
            return temp

        raise IRError(f"unsupported expression {type(expr)}")

def lower_source(src: str) -> ModuleIR:
    return Lowerer().lower_module(F.parse_source(src))

def format_ir(module: ModuleIR) -> str:
    out: list[str] = []
    for fn in module.functions:
        out.append(f"fn {fn.name}({', '.join(fn.params)})")
        for block in fn.blocks:
            out.append(f"{block.label}:")
            for ins in block.instrs:
                lhs = f"{ins.dst} = " if ins.dst else ""
                out.append(f"  {lhs}{ins.op} {' '.join(ins.args)}".rstrip())
            if block.term:
                out.append(f"  {block.term.op} {' '.join(block.term.args)}".rstrip())
    return "\n".join(out)

def successors(fn: FunctionIR) -> dict[str, list[str]]:
    result = {block.label: [] for block in fn.blocks}
    for block in fn.blocks:
        if not block.term:
            continue
        if block.term.op == "jump":
            result[block.label] = [block.term.args[0]]
        elif block.term.op == "cjump":
            result[block.label] = block.term.args[1:3]
    return result

def predecessors(fn: FunctionIR) -> dict[str, list[str]]:
    succ = successors(fn)
    result = {block.label: [] for block in fn.blocks}
    for source, targets in succ.items():
        for target in targets:
            if target not in result:
                raise IRError(f"unknown block target {target!r} from {source!r}")
            result[target].append(source)
    return result

def dominators(fn: FunctionIR) -> dict[str, set[str]]:
    labels = [block.label for block in fn.blocks]
    if not labels:
        return {}

    preds = predecessors(fn)
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

def uses_defs_block(block: Block) -> tuple[set[str], set[str]]:
    uses: set[str] = set()
    defs: set[str] = set()

    for ins in block.instrs:
        if ins.op in ("call", "bin", "cmp"):
            values = ins.args[1:]
        elif ins.op in ("mov", "un"):
            values = ins.args[-1:]
        else:
            values = []

        for value in values:
            if (value.startswith("%") or value.isidentifier()) and value not in defs:
                uses.add(value)
        if ins.dst:
            defs.add(ins.dst)

    if block.term and block.term.op in ("ret", "cjump"):
        value = block.term.args[0]
        if value not in defs:
            uses.add(value)

    return uses, defs

def liveness(
    fn: FunctionIR,
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    labels = [block.label for block in fn.blocks]
    block_map = {block.label: block for block in fn.blocks}
    succ = successors(fn)
    live_in = {label: set() for label in labels}
    live_out = {label: set() for label in labels}

    changed = True
    while changed:
        changed = False
        for label in reversed(labels):
            uses, defs = uses_defs_block(block_map[label])
            new_out = (
                set().union(*(live_in[target] for target in succ[label]))
                if succ[label]
                else set()
            )
            new_in = uses | (new_out - defs)
            if new_out != live_out[label] or new_in != live_in[label]:
                live_out[label] = new_out
                live_in[label] = new_in
                changed = True

    return live_in, live_out

def _fold_binary(op: str, a: int, b: int) -> Optional[int]:
    if op == "+":
        return wrap_i64(a + b)
    if op == "-":
        return wrap_i64(a - b)
    if op == "*":
        return wrap_i64(a * b)

    if op in ("/", "%"):
        try:
            return trunc_div_i64(a, b) if op == "/" else trunc_mod_i64(a, b)
        except (ZeroDivisionError, OverflowError):
            # Preserve the runtime trap instead of changing program semantics.
            return None

    return None

def optimize_local(fn: FunctionIR) -> None:
    for block in fn.blocks:
        constants: dict[str, int] = {}
        new_instrs: list[Instr] = []

        for ins in block.instrs:
            if ins.op == "const" and ins.dst is not None:
                constants[ins.dst] = wrap_i64(int(ins.args[0]))
                new_instrs.append(
                    Instr("const", ins.dst, [str(constants[ins.dst])])
                )
                continue

            if (
                ins.op == "mov"
                and ins.dst is not None
                and ins.args[0] in constants
            ):
                value = constants[ins.args[0]]
                constants[ins.dst] = value
                new_instrs.append(Instr("const", ins.dst, [str(value)]))
                continue

            if (
                ins.op == "bin"
                and ins.dst is not None
                and ins.args[1] in constants
                and ins.args[2] in constants
            ):
                left = constants[ins.args[1]]
                right = constants[ins.args[2]]
                folded = _fold_binary(ins.args[0], left, right)
                if folded is not None:
                    constants[ins.dst] = folded
                    new_instrs.append(Instr("const", ins.dst, [str(folded)]))
                    continue

            if ins.dst is not None:
                constants.pop(ins.dst, None)
            new_instrs.append(ins)

        block.instrs = new_instrs

def ssa_phi_candidates(fn: FunctionIR) -> dict[str, list[str]]:
    """Educational phi-placement hint only; this is not full SSA construction."""
    preds = predecessors(fn)
    block_map = {block.label: block for block in fn.blocks}
    result: dict[str, list[str]] = {}

    for label, incoming in preds.items():
        if len(incoming) < 2:
            continue
        defs_by_pred = [uses_defs_block(block_map[pred])[1] for pred in incoming]
        names = set().union(*defs_by_pred)
        candidates = sorted(
            name
            for name in names
            if sum(name in defs for defs in defs_by_pred) >= 2
            and not name.startswith("%")
        )
        if candidates:
            result[label] = candidates

    return result

def main(argv: Optional[list[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(
            "usage: elite_ir.py [--ir|--dom|--live|--phi-candidates|--ssa|--opt] FILE",
            file=sys.stderr,
        )
        return 2

    mode = "--ir"
    if args[0].startswith("--"):
        mode = args.pop(0)
    if len(args) != 1:
        return 2

    try:
        module = lower_source(open(args[0], encoding="utf-8").read())

        if mode == "--opt":
            for fn in module.functions:
                optimize_local(fn)
            print(format_ir(module))
            return 0

        if mode == "--ir":
            print(format_ir(module))
            return 0

        for fn in module.functions:
            print(f"function {fn.name}")
            if mode == "--dom":
                for block, dom in dominators(fn).items():
                    print(block, ":", ",".join(sorted(dom)))
            elif mode == "--live":
                live_in, live_out = liveness(fn)
                for block in live_in:
                    print(
                        block,
                        "in=",
                        sorted(live_in[block]),
                        "out=",
                        sorted(live_out[block]),
                    )
            elif mode == "--phi-candidates":
                print(json.dumps(ssa_phi_candidates(fn), sort_keys=True))
            elif mode == "--ssa":
                import elite_ssa
                print(elite_ssa.format_ssa(fn))
            else:
                raise IRError("unknown mode")

        return 0

    except (OSError, F.CompileError, IRError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
import sys
from typing import Optional, Union

INT64_MIN = -(1 << 63)
INT64_MAX = (1 << 63) - 1

class CompileError(Exception):
    pass

@dataclass
class Token:
    kind: str
    text: str
    pos: int

KEYWORDS = {"fn", "let", "return", "if", "else", "while", "true", "false", "int", "bool"}
TOKEN_RE = re.compile(
    r"""\s+|//[^\n]*|->|==|!=|<=|>=|&&|\|\||[A-Za-z_][A-Za-z0-9_]*|[0-9]+|[+\-*/%<>=!():;,{}]"""
)

def lex(src: str) -> list[Token]:
    tokens: list[Token] = []
    pos = 0
    while pos < len(src):
        match = TOKEN_RE.match(src, pos)
        if not match:
            raise CompileError(f"unexpected character at byte {pos}: {src[pos]!r}")

        text = match.group(0)
        start = pos
        pos = match.end()

        if text.isspace() or text.startswith("//"):
            continue
        if text.isdigit():
            kind = "INT"
        elif re.match(r"^[A-Za-z_]", text):
            kind = text.upper() if text in KEYWORDS else "IDENT"
        else:
            kind = text

        tokens.append(Token(kind, text, start))

    tokens.append(Token("EOF", "", len(src)))
    return tokens

@dataclass
class Program:
    functions: list["Function"]

@dataclass
class Function:
    name: str
    params: list["Param"]
    ret_type: str
    body: "Block"

@dataclass
class Param:
    name: str
    type_name: str

@dataclass
class Block:
    statements: list["Stmt"]

@dataclass
class Let:
    name: str
    type_name: str
    value: "Expr"

@dataclass
class Assign:
    name: str
    value: "Expr"

@dataclass
class Return:
    value: "Expr"

@dataclass
class If:
    cond: "Expr"
    then_block: Block
    else_block: Optional[Block]

@dataclass
class While:
    cond: "Expr"
    body: Block

@dataclass
class ExprStmt:
    value: "Expr"

Stmt = Union[Let, Assign, Return, If, While, ExprStmt]

@dataclass
class IntLit:
    value: int

@dataclass
class BoolLit:
    value: bool

@dataclass
class Var:
    name: str

@dataclass
class Unary:
    op: str
    expr: "Expr"

@dataclass
class Binary:
    op: str
    left: "Expr"
    right: "Expr"

@dataclass
class Call:
    name: str
    args: list["Expr"]

Expr = Union[IntLit, BoolLit, Var, Unary, Binary, Call]

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index = 0

    def current(self) -> Token:
        return self.tokens[self.index]

    def eat(self, kind: str) -> Token:
        token = self.current()
        if token.kind != kind:
            raise CompileError(
                f"expected {kind} at byte {token.pos}, got {token.kind}"
            )
        self.index += 1
        return token

    def maybe(self, kind: str) -> Optional[Token]:
        if self.current().kind == kind:
            return self.eat(kind)
        return None

    def parse_program(self) -> Program:
        functions: list[Function] = []
        while self.current().kind != "EOF":
            functions.append(self.parse_function())
        if not functions:
            raise CompileError("program must define at least one function")
        return Program(functions)

    def parse_function(self) -> Function:
        self.eat("FN")
        name = self.eat("IDENT").text
        self.eat("(")

        params: list[Param] = []
        if self.current().kind != ")":
            while True:
                param_name = self.eat("IDENT").text
                self.eat(":")
                params.append(Param(param_name, self.parse_type()))
                if not self.maybe(","):
                    break

        self.eat(")")
        self.eat("->")
        ret_type = self.parse_type()
        return Function(name, params, ret_type, self.parse_block())

    def parse_type(self) -> str:
        if self.current().kind in ("INT", "BOOL"):
            return self.eat(self.current().kind).text
        raise CompileError(f"expected type at byte {self.current().pos}")

    def parse_block(self) -> Block:
        self.eat("{")
        statements: list[Stmt] = []
        while self.current().kind != "}":
            if self.current().kind == "EOF":
                raise CompileError("unterminated block")
            statements.append(self.parse_statement())
        self.eat("}")
        return Block(statements)

    def parse_statement(self) -> Stmt:
        kind = self.current().kind

        if kind == "LET":
            self.eat("LET")
            name = self.eat("IDENT").text
            self.eat(":")
            type_name = self.parse_type()
            self.eat("=")
            value = self.parse_expression()
            self.eat(";")
            return Let(name, type_name, value)

        if kind == "RETURN":
            self.eat("RETURN")
            value = self.parse_expression()
            self.eat(";")
            return Return(value)

        if kind == "IF":
            self.eat("IF")
            self.eat("(")
            condition = self.parse_expression()
            self.eat(")")
            then_block = self.parse_block()
            else_block = self.parse_block() if self.maybe("ELSE") else None
            return If(condition, then_block, else_block)

        if kind == "WHILE":
            self.eat("WHILE")
            self.eat("(")
            condition = self.parse_expression()
            self.eat(")")
            return While(condition, self.parse_block())

        if kind == "IDENT" and self.tokens[self.index + 1].kind == "=":
            name = self.eat("IDENT").text
            self.eat("=")
            value = self.parse_expression()
            self.eat(";")
            return Assign(name, value)

        value = self.parse_expression()
        self.eat(";")
        return ExprStmt(value)

    def parse_expression(self) -> Expr:
        return self.parse_logical_or()

    def parse_logical_or(self) -> Expr:
        expr = self.parse_logical_and()
        while self.maybe("||"):
            expr = Binary("||", expr, self.parse_logical_and())
        return expr

    def parse_logical_and(self) -> Expr:
        expr = self.parse_equality()
        while self.maybe("&&"):
            expr = Binary("&&", expr, self.parse_equality())
        return expr

    def parse_equality(self) -> Expr:
        expr = self.parse_relational()
        while self.current().kind in ("==", "!="):
            op = self.eat(self.current().kind).text
            expr = Binary(op, expr, self.parse_relational())
        return expr

    def parse_relational(self) -> Expr:
        expr = self.parse_additive()
        while self.current().kind in ("<", "<=", ">", ">="):
            op = self.eat(self.current().kind).text
            expr = Binary(op, expr, self.parse_additive())
        return expr

    def parse_additive(self) -> Expr:
        expr = self.parse_multiplicative()
        while self.current().kind in ("+", "-"):
            op = self.eat(self.current().kind).text
            expr = Binary(op, expr, self.parse_multiplicative())
        return expr

    def parse_multiplicative(self) -> Expr:
        expr = self.parse_unary()
        while self.current().kind in ("*", "/", "%"):
            op = self.eat(self.current().kind).text
            expr = Binary(op, expr, self.parse_unary())
        return expr

    def parse_unary(self) -> Expr:
        if self.current().kind in ("!", "-"):
            op = self.eat(self.current().kind).text
            return Unary(op, self.parse_unary())
        return self.parse_primary()

    def parse_primary(self) -> Expr:
        token = self.current()

        if token.kind == "INT":
            self.index += 1
            value = int(token.text)
            if value > INT64_MAX:
                raise CompileError(
                    f"integer literal out of signed 64-bit range at byte {token.pos}: {token.text}"
                )
            return IntLit(value)

        if token.kind == "TRUE":
            self.index += 1
            return BoolLit(True)

        if token.kind == "FALSE":
            self.index += 1
            return BoolLit(False)

        if token.kind == "IDENT":
            self.index += 1
            name = token.text
            if self.maybe("("):
                args: list[Expr] = []
                if self.current().kind != ")":
                    while True:
                        args.append(self.parse_expression())
                        if not self.maybe(","):
                            break
                self.eat(")")
                return Call(name, args)
            return Var(name)

        if self.maybe("("):
            expr = self.parse_expression()
            self.eat(")")
            return expr

        raise CompileError(f"expected expression at byte {token.pos}")

def block_returns(block: Block) -> bool:
    for statement in block.statements:
        if isinstance(statement, Return):
            return True
        if (
            isinstance(statement, If)
            and statement.else_block is not None
            and block_returns(statement.then_block)
            and block_returns(statement.else_block)
        ):
            return True
    return False

class Checker:
    def __init__(self, program: Program):
        self.program = program
        self.signatures: dict[str, tuple[list[str], str]] = {}

    def check(self) -> None:
        for function in self.program.functions:
            if function.name in self.signatures:
                raise CompileError(f"duplicate function {function.name}")

            seen: set[str] = set()
            for param in function.params:
                if param.name in seen:
                    raise CompileError(
                        f"duplicate parameter {param.name} in {function.name}"
                    )
                seen.add(param.name)

            self.signatures[function.name] = (
                [param.type_name for param in function.params],
                function.ret_type,
            )

        if "main" not in self.signatures:
            raise CompileError("program must define main")

        main_params, main_return = self.signatures["main"]
        if main_params or main_return != "int":
            raise CompileError("main must have signature: fn main() -> int")

        for function in self.program.functions:
            self.check_function(function)

    def check_function(self, function: Function) -> None:
        env = {param.name: param.type_name for param in function.params}
        self.check_block(function.body, env, function.ret_type)
        if not block_returns(function.body):
            raise CompileError(
                f"function {function.name} does not return on all obvious paths"
            )

    def check_block(
        self, block: Block, env: dict[str, str], return_type: str
    ) -> None:
        local = dict(env)

        for statement in block.statements:
            if isinstance(statement, Let):
                if statement.name in local:
                    raise CompileError(
                        f"duplicate/shadowed variable {statement.name}"
                    )
                actual = self.type_expression(statement.value, local)
                if actual != statement.type_name:
                    raise CompileError(
                        f"let {statement.name}: expected {statement.type_name}, got {actual}"
                    )
                local[statement.name] = statement.type_name

            elif isinstance(statement, Assign):
                if statement.name not in local:
                    raise CompileError(
                        f"assignment to unknown variable {statement.name}"
                    )
                actual = self.type_expression(statement.value, local)
                if actual != local[statement.name]:
                    raise CompileError(
                        f"assignment {statement.name}: "
                        f"expected {local[statement.name]}, got {actual}"
                    )

            elif isinstance(statement, Return):
                actual = self.type_expression(statement.value, local)
                if actual != return_type:
                    raise CompileError(
                        f"return expected {return_type}, got {actual}"
                    )

            elif isinstance(statement, If):
                if self.type_expression(statement.cond, local) != "bool":
                    raise CompileError("if condition must be bool")
                self.check_block(statement.then_block, local, return_type)
                if statement.else_block:
                    self.check_block(statement.else_block, local, return_type)

            elif isinstance(statement, While):
                if self.type_expression(statement.cond, local) != "bool":
                    raise CompileError("while condition must be bool")
                self.check_block(statement.body, local, return_type)

            elif isinstance(statement, ExprStmt):
                self.type_expression(statement.value, local)

    def type_expression(self, expr: Expr, env: dict[str, str]) -> str:
        if isinstance(expr, IntLit):
            return "int"
        if isinstance(expr, BoolLit):
            return "bool"

        if isinstance(expr, Var):
            if expr.name not in env:
                raise CompileError(f"unknown variable {expr.name}")
            return env[expr.name]

        if isinstance(expr, Unary):
            actual = self.type_expression(expr.expr, env)
            if expr.op == "-" and actual == "int":
                return "int"
            if expr.op == "!" and actual == "bool":
                return "bool"
            raise CompileError(f"bad unary {expr.op} for {actual}")

        if isinstance(expr, Binary):
            left = self.type_expression(expr.left, env)
            right = self.type_expression(expr.right, env)

            if expr.op in ("+", "-", "*", "/", "%") and left == right == "int":
                return "int"
            if expr.op in ("<", "<=", ">", ">=") and left == right == "int":
                return "bool"
            if expr.op in ("==", "!=") and left == right:
                return "bool"
            if expr.op in ("&&", "||") and left == right == "bool":
                return "bool"

            raise CompileError(f"bad binary {expr.op} for {left},{right}")

        if isinstance(expr, Call):
            if expr.name not in self.signatures:
                raise CompileError(f"unknown function {expr.name}")

            params, return_type = self.signatures[expr.name]
            if len(params) != len(expr.args):
                raise CompileError(
                    f"{expr.name} expects {len(params)} args, got {len(expr.args)}"
                )

            for index, (expected, arg) in enumerate(zip(params, expr.args), 1):
                actual = self.type_expression(arg, env)
                if actual != expected:
                    raise CompileError(
                        f"{expr.name} arg {index}: expected {expected}, got {actual}"
                    )
            return return_type

        raise AssertionError(type(expr))

def parse_source(src: str) -> Program:
    program = Parser(lex(src)).parse_program()
    Checker(program).check()
    return program

def ast_json(program: Program) -> str:
    return json.dumps(asdict(program), indent=2)

def main(argv: Optional[list[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(
            "usage: elite_frontend.py [--tokens|--ast|--check] FILE",
            file=sys.stderr,
        )
        return 2

    mode = "--check"
    if args[0].startswith("--"):
        mode = args.pop(0)

    if len(args) != 1:
        print("expected one source file", file=sys.stderr)
        return 2

    try:
        src = open(args[0], encoding="utf-8").read()
        if mode == "--tokens":
            for token in lex(src):
                print(f"{token.kind:10} {token.text!r} @{token.pos}")
            return 0

        program = parse_source(src)
        if mode == "--ast":
            print(ast_json(program))
        elif mode == "--check":
            print("OK")
        else:
            raise CompileError(f"unknown mode {mode}")
        return 0

    except (OSError, CompileError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

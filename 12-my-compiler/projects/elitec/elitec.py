#!/usr/bin/env python3
from __future__ import annotations
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "09-compiler-frontend" / "projects" / "elite-frontend"))
sys.path.insert(0, str(ROOT / "10-compiler-ir" / "projects" / "elite-ir"))
sys.path.insert(0, str(ROOT / "11-compiler-backend" / "projects" / "elite-backend"))

import elite_frontend as F
import elite_ir as I
import elite_backend as B

VERSION = "0.1.0"

def read_source(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def emit_tokens(src: str) -> str:
    return "\n".join(f"{t.kind:10} {t.text!r} @{t.pos}" for t in F.lex(src)) + "\n"

def emit_ir(src: str, optimize: bool) -> str:
    mod = I.lower_source(src)
    if optimize:
        for fn in mod.functions:
            I.optimize_local(fn)
    return I.format_ir(mod) + "\n"

def compile_executable(src: str, output: Path, cc: str, optimize: bool) -> None:
    asm = B.compile_source(src, optimize)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="elitec-") as td:
        asm_path = Path(td) / "program.s"
        asm_path.write_text(asm, encoding="utf-8")
        proc = subprocess.run([cc, str(asm_path), "-o", str(output)], text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"assembler/linker driver failed with status {proc.returncode}")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="elitec", description="EliteLang educational compiler")
    p.add_argument("source", nargs="?")
    p.add_argument("-o", "--output", default="a.out")
    p.add_argument("--check", action="store_true")
    p.add_argument("--emit", choices=("tokens", "ast", "ir", "asm"))
    p.add_argument("--opt", action="store_true")
    p.add_argument("--run", action="store_true")
    p.add_argument("--cc", default=os.environ.get("CC", "gcc"))
    p.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if not args.source:
        print("elitec: source file is required", file=sys.stderr)
        return 2
    try:
        src = read_source(args.source)
        if args.emit == "tokens":
            sys.stdout.write(emit_tokens(src))
            return 0
        program = F.parse_source(src)
        if args.check:
            print("OK")
            return 0
        if args.emit == "ast":
            print(F.ast_json(program))
            return 0
        if args.emit == "ir":
            sys.stdout.write(emit_ir(src, args.opt))
            return 0
        if args.emit == "asm":
            sys.stdout.write(B.compile_source(src, args.opt))
            return 0

        output = Path(args.output).resolve()
        compile_executable(src, output, args.cc, args.opt)
        if args.run:
            result = subprocess.run([str(output)])
            return result.returncode
        return 0
    except (OSError, F.CompileError, I.IRError, B.BackendError, RuntimeError) as exc:
        print(f"elitec: error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

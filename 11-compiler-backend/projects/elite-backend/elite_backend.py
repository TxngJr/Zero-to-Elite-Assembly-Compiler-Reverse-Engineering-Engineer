#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"09-compiler-frontend"/"projects"/"elite-frontend"))
sys.path.insert(0,str(ROOT/"10-compiler-ir"/"projects"/"elite-ir"))
import elite_frontend as F
import elite_ir as I

class BackendError(Exception): pass
ARGREGS=["rdi","rsi","rdx","rcx","r8","r9"]

class Codegen:
    def __init__(self,mod): self.mod=mod; self.lines=[]
    def emit(self,s=""): self.lines.append(s)
    def slots(self,fn):
        names=[]; seen=set()
        def add(n):
            if (n.startswith("%") or n.isidentifier()) and n not in seen:
                seen.add(n); names.append(n)
        for p in fn.params: add(p)
        for b in fn.blocks:
            for ins in b.instrs:
                if ins.dst: add(ins.dst)
                args=ins.args[1:] if ins.op=="call" else ins.args
                for a in args:
                    if a.startswith("%") or a.isidentifier(): add(a)
            if b.term and b.term.op in ("ret","cjump"): add(b.term.args[0])
        return {n:8*(i+1) for i,n in enumerate(names)}
    def load(self,n,r,s): self.emit(f"    mov {r}, QWORD PTR [rbp-{s[n]}]")
    def store(self,n,r,s): self.emit(f"    mov QWORD PTR [rbp-{s[n]}], {r}")
    def gen(self):
        self.emit(".intel_syntax noprefix"); self.emit(".text")
        for fn in self.mod.functions: self.gen_fn(fn)
        self.emit('.section .note.GNU-stack,"",@progbits')
        return "\n".join(self.lines)+"\n"
    def gen_fn(self,fn):
        s=self.slots(fn); frame=((len(s)*8+15)//16)*16
        self.emit(f".global {fn.name}"); self.emit(f".type {fn.name}, @function"); self.emit(f"{fn.name}:")
        self.emit("    push rbp"); self.emit("    mov rbp, rsp")
        if frame: self.emit(f"    sub rsp, {frame}")
        for i,p in enumerate(fn.params):
            if i<6: self.store(p,ARGREGS[i],s)
            else:
                self.emit(f"    mov rax, QWORD PTR [rbp+{16+8*(i-6)}]"); self.store(p,"rax",s)
        for b in fn.blocks:
            self.emit(f".L_{fn.name}_{b.label}:")
            for ins in b.instrs: self.gen_ins(ins,s)
            if b.term: self.gen_term(fn.name,b.term,s)
        self.emit(f".L_{fn.name}_fallthrough:"); self.emit("    xor eax, eax"); self.emit("    leave"); self.emit("    ret")
        self.emit(f".size {fn.name}, .-{fn.name}"); self.emit()
    def gen_ins(self,i,s):
        if i.op=="const":
            self.emit(f"    mov rax, {int(i.args[0])}"); self.store(i.dst,"rax",s)
        elif i.op=="mov":
            self.load(i.args[0],"rax",s); self.store(i.dst,"rax",s)
        elif i.op=="un":
            op,a=i.args; self.load(a,"rax",s)
            if op=="-": self.emit("    neg rax")
            elif op=="!":
                self.emit("    test rax, rax"); self.emit("    sete al"); self.emit("    movzx rax, al")
            else: raise BackendError(op)
            self.store(i.dst,"rax",s)
        elif i.op in ("bin","cmp"):
            op,a,b=i.args; self.load(a,"rax",s); self.load(b,"rcx",s)
            if i.op=="bin":
                if op=="+": self.emit("    add rax, rcx")
                elif op=="-": self.emit("    sub rax, rcx")
                elif op=="*": self.emit("    imul rax, rcx")
                elif op in ("/","%"):
                    self.emit("    cqo"); self.emit("    idiv rcx")
                    if op=="%": self.emit("    mov rax, rdx")
                else: raise BackendError(op)
            else:
                self.emit("    cmp rax, rcx")
                cc={"<":"l","<=":"le",">":"g",">=":"ge","==":"e","!=":"ne"}[op]
                self.emit(f"    set{cc} al"); self.emit("    movzx rax, al")
            self.store(i.dst,"rax",s)
        elif i.op=="call":
            fn=i.args[0]; args=i.args[1:]; nstack=max(0,len(args)-6); pad=8 if nstack%2 else 0
            if pad: self.emit("    sub rsp, 8")
            for a in reversed(args[6:]):
                self.load(a,"rax",s); self.emit("    push rax")
            for idx,a in enumerate(args[:6]): self.load(a,ARGREGS[idx],s)
            self.emit(f"    call {fn}")
            cleanup=nstack*8+pad
            if cleanup: self.emit(f"    add rsp, {cleanup}")
            self.store(i.dst,"rax",s)
        else: raise BackendError(i.op)
    def gen_term(self,fn,t,s):
        if t.op=="ret":
            self.load(t.args[0],"rax",s); self.emit("    leave"); self.emit("    ret")
        elif t.op=="jump": self.emit(f"    jmp .L_{fn}_{t.args[0]}")
        elif t.op=="cjump":
            self.load(t.args[0],"rax",s); self.emit("    test rax, rax")
            self.emit(f"    jne .L_{fn}_{t.args[1]}"); self.emit(f"    jmp .L_{fn}_{t.args[2]}")
        else: raise BackendError(t.op)

def compile_source(src,opt=False):
    mod=I.lower_source(src)
    if opt:
        for fn in mod.functions: I.optimize_local(fn)
    return Codegen(mod).gen()

def main(argv=None):
    argv=sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage: elite_backend.py [--opt] SOURCE [-o assembly.s]",file=sys.stderr); return 2
    opt=False
    if argv and argv[0]=="--opt": opt=True; argv.pop(0)
    out=None
    if "-o" in argv:
        j=argv.index("-o")
        if j+1>=len(argv): return 2
        out=argv[j+1]; del argv[j:j+2]
    if len(argv)!=1: return 2
    try:
        asm=compile_source(open(argv[0],encoding="utf-8").read(),opt)
        if out: open(out,"w",encoding="utf-8").write(asm)
        else: print(asm,end="")
        return 0
    except (OSError,F.CompileError,I.IRError,BackendError) as e:
        print(f"error: {e}",file=sys.stderr); return 1

if __name__=="__main__": raise SystemExit(main())

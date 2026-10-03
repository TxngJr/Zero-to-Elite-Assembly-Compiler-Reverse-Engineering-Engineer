#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "09-compiler-frontend" / "projects" / "elite-frontend"))
import elite_frontend as F

class IRError(Exception): pass
@dataclass
class Instr: op:str; dst:Optional[str]=None; args:list[str]=field(default_factory=list)
@dataclass
class Block: label:str; instrs:list[Instr]=field(default_factory=list); term:Optional[Instr]=None
@dataclass
class FunctionIR: name:str; params:list[str]; blocks:list[Block]
@dataclass
class ModuleIR: functions:list[FunctionIR]

class Lowerer:
    def __init__(self): self.temp=0; self.label=0; self.blocks=[]; self.cur=None
    def nt(self): self.temp+=1; return f"%t{self.temp}"
    def nl(self,p="bb"): self.label+=1; return f"{p}{self.label}"
    def add_block(self,label=None):
        b=Block(label or self.nl()); self.blocks.append(b); self.cur=b; return b
    def emit(self,op,dst=None,*args):
        ins=Instr(op,dst,list(args)); self.cur.instrs.append(ins); return dst
    def term(self,op,*args): self.cur.term=Instr(op,None,list(args))
    def lower_module(self,p): return ModuleIR([self.lower_fn(fn) for fn in p.functions])
    def lower_fn(self,fn):
        self.temp=0; self.label=0; self.blocks=[]; self.add_block("entry")
        for s in fn.body.statements:
            if self.cur.term is None: self.lower_stmt(s)
        return FunctionIR(fn.name,[p.name for p in fn.params],self.blocks)
    def lower_stmt(self,s):
        if isinstance(s,F.Let): self.emit("mov",s.name,self.lower_expr(s.value))
        elif isinstance(s,F.Assign): self.emit("mov",s.name,self.lower_expr(s.value))
        elif isinstance(s,F.ExprStmt): self.lower_expr(s.value)
        elif isinstance(s,F.Return): self.term("ret",self.lower_expr(s.value))
        elif isinstance(s,F.If):
            cond=self.lower_expr(s.cond); a=self.nl("then"); b=self.nl("else"); z=self.nl("ifend")
            self.term("cjump",cond,a,b)
            self.add_block(a)
            for x in s.then_block.statements:
                if self.cur.term is None: self.lower_stmt(x)
            if self.cur.term is None: self.term("jump",z)
            self.add_block(b)
            if s.else_block:
                for x in s.else_block.statements:
                    if self.cur.term is None: self.lower_stmt(x)
            if self.cur.term is None: self.term("jump",z)
            self.add_block(z)
        elif isinstance(s,F.While):
            c=self.nl("while_cond"); body=self.nl("while_body"); end=self.nl("while_end")
            self.term("jump",c); self.add_block(c); v=self.lower_expr(s.cond); self.term("cjump",v,body,end)
            self.add_block(body)
            for x in s.body.statements:
                if self.cur.term is None: self.lower_stmt(x)
            if self.cur.term is None: self.term("jump",c)
            self.add_block(end)
        else: raise IRError(f"unsupported stmt {type(s)}")
    def lower_expr(self,e):
        if isinstance(e,F.IntLit):
            t=self.nt(); self.emit("const",t,str(e.value)); return t
        if isinstance(e,F.BoolLit):
            t=self.nt(); self.emit("const",t,"1" if e.value else "0"); return t
        if isinstance(e,F.Var): return e.name
        if isinstance(e,F.Unary):
            a=self.lower_expr(e.expr); t=self.nt(); self.emit("un",t,e.op,a); return t
        if isinstance(e,F.Call):
            args=[self.lower_expr(a) for a in e.args]; t=self.nt(); self.emit("call",t,e.name,*args); return t
        if isinstance(e,F.Binary) and e.op in ("&&","||"):
            result=self.nt(); left=self.lower_expr(e.left); rhs=self.nl("logic_rhs"); short=self.nl("logic_short"); done=self.nl("logic_done")
            self.term("cjump",left,rhs,short) if e.op=="&&" else self.term("cjump",left,short,rhs)
            self.add_block(rhs); rv=self.lower_expr(e.right); self.emit("mov",result,rv); self.term("jump",done)
            self.add_block(short); c=self.nt(); self.emit("const",c,"0" if e.op=="&&" else "1"); self.emit("mov",result,c); self.term("jump",done)
            self.add_block(done); return result
        if isinstance(e,F.Binary):
            a=self.lower_expr(e.left); b=self.lower_expr(e.right); t=self.nt()
            self.emit("cmp" if e.op in ("<","<=",">",">=","==","!=") else "bin",t,e.op,a,b); return t
        raise IRError(f"unsupported expr {type(e)}")

def lower_source(src): return Lowerer().lower_module(F.parse_source(src))

def format_ir(m):
    out=[]
    for fn in m.functions:
        out.append(f"fn {fn.name}({', '.join(fn.params)})")
        for b in fn.blocks:
            out.append(f"{b.label}:")
            for i in b.instrs:
                lhs=f"{i.dst} = " if i.dst else ""
                out.append(f"  {lhs}{i.op} {' '.join(i.args)}".rstrip())
            if b.term: out.append(f"  {b.term.op} {' '.join(b.term.args)}".rstrip())
    return "\n".join(out)

def succs(fn):
    d={b.label:[] for b in fn.blocks}
    for b in fn.blocks:
        if not b.term: continue
        if b.term.op=="jump": d[b.label]=[b.term.args[0]]
        elif b.term.op=="cjump": d[b.label]=b.term.args[1:3]
    return d

def predecessors(fn):
    s=succs(fn); p={b.label:[] for b in fn.blocks}
    for a,targets in s.items():
        for z in targets: p[z].append(a)
    return p

def dominators(fn):
    labels=[b.label for b in fn.blocks]; preds=predecessors(fn); entry=labels[0]
    dom={l:set(labels) for l in labels}; dom[entry]={entry}
    changed=True
    while changed:
        changed=False
        for l in labels[1:]:
            ps=preds[l]; new={l}|(set.intersection(*(dom[x] for x in ps)) if ps else set())
            if new!=dom[l]: dom[l]=new; changed=True
    return dom

def uses_defs_block(b):
    uses=set(); defs=set()
    for i in b.instrs:
        vals=i.args[1:] if i.op in ("call","bin","cmp") else i.args[-1:] if i.op in ("mov","un") else []
        for v in vals:
            if (v.startswith("%") or v.isidentifier()) and v not in defs: uses.add(v)
        if i.dst: defs.add(i.dst)
    if b.term and b.term.op in ("ret","cjump"):
        v=b.term.args[0]
        if v not in defs: uses.add(v)
    return uses,defs

def liveness(fn):
    labels=[b.label for b in fn.blocks]; bm={b.label:b for b in fn.blocks}; s=succs(fn)
    inn={l:set() for l in labels}; out={l:set() for l in labels}
    changed=True
    while changed:
        changed=False
        for l in reversed(labels):
            u,d=uses_defs_block(bm[l]); no=set().union(*(inn[x] for x in s[l])) if s[l] else set(); ni=u|(no-d)
            if no!=out[l] or ni!=inn[l]: out[l]=no; inn[l]=ni; changed=True
    return inn,out

def optimize_local(fn):
    for b in fn.blocks:
        const={}; new=[]
        for i in b.instrs:
            if i.op=="const": const[i.dst]=int(i.args[0]); new.append(i); continue
            if i.op=="mov" and i.args[0] in const:
                v=const[i.args[0]]; const[i.dst]=v; new.append(Instr("const",i.dst,[str(v)])); continue
            if i.op=="bin" and i.args[1] in const and i.args[2] in const:
                a,c=const[i.args[1]],const[i.args[2]]; op=i.args[0]
                if op=="+": v=a+c
                elif op=="-": v=a-c
                elif op=="*": v=a*c
                elif op=="/" and c!=0: v=int(a/c)
                elif op=="%" and c!=0: v=a-int(a/c)*c
                else: new.append(i); const.pop(i.dst,None); continue
                const[i.dst]=v; new.append(Instr("const",i.dst,[str(v)])); continue
            if i.dst: const.pop(i.dst,None)
            new.append(i)
        b.instrs=new
    return fn

def ssa_phi_candidates(fn):
    preds=predecessors(fn); bm={b.label:b for b in fn.blocks}; out={}
    for label,ps in preds.items():
        if len(ps)<2: continue
        defs_by=[uses_defs_block(bm[p])[1] for p in ps]
        names=set().union(*defs_by)
        cand=sorted(n for n in names if sum(n in d for d in defs_by)>=2 and not n.startswith("%"))
        if cand: out[label]=cand
    return out

def main(argv=None):
    argv=sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage: elite_ir.py [--ir|--dom|--live|--ssa|--opt] FILE",file=sys.stderr); return 2
    mode="--ir"
    if argv[0].startswith("--"): mode=argv.pop(0)
    if len(argv)!=1: return 2
    try:
        m=lower_source(open(argv[0],encoding="utf-8").read())
        if mode=="--opt":
            for fn in m.functions: optimize_local(fn)
            print(format_ir(m)); return 0
        if mode=="--ir": print(format_ir(m)); return 0
        for fn in m.functions:
            print(f"function {fn.name}")
            if mode=="--dom":
                for b,d in dominators(fn).items(): print(b,":",",".join(sorted(d)))
            elif mode=="--live":
                li,lo=liveness(fn)
                for b in li: print(b,"in=",sorted(li[b]),"out=",sorted(lo[b]))
            elif mode=="--ssa": print(json.dumps(ssa_phi_candidates(fn),sort_keys=True))
            else: raise IRError("unknown mode")
        return 0
    except (OSError,F.CompileError,IRError) as e:
        print(f"error: {e}",file=sys.stderr); return 1

if __name__=="__main__": raise SystemExit(main())

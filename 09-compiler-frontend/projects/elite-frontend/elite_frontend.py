#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Optional, Union
import json, re, sys

class CompileError(Exception): pass
@dataclass
class Token: kind:str; text:str; pos:int

KEYWORDS={"fn","let","return","if","else","while","true","false","int","bool"}
TOKEN_RE=re.compile(r'''\s+|//[^\n]*|->|==|!=|<=|>=|&&|\|\||[A-Za-z_][A-Za-z0-9_]*|[0-9]+|[+\-*/%<>=!():;,{}]''')

def lex(src:str)->List[Token]:
    out=[]; pos=0
    while pos<len(src):
        m=TOKEN_RE.match(src,pos)
        if not m: raise CompileError(f"unexpected character at byte {pos}: {src[pos]!r}")
        text=m.group(0); start=pos; pos=m.end()
        if text.isspace() or text.startswith("//"): continue
        if text.isdigit(): kind="INT"
        elif re.match(r"^[A-Za-z_]",text): kind=text.upper() if text in KEYWORDS else "IDENT"
        else: kind=text
        out.append(Token(kind,text,start))
    out.append(Token("EOF","",len(src))); return out

@dataclass
class Program: functions:list["Function"]
@dataclass
class Function: name:str; params:list["Param"]; ret_type:str; body:"Block"
@dataclass
class Param: name:str; type_name:str
@dataclass
class Block: statements:list["Stmt"]
@dataclass
class Let: name:str; type_name:str; value:"Expr"
@dataclass
class Assign: name:str; value:"Expr"
@dataclass
class Return: value:"Expr"
@dataclass
class If: cond:"Expr"; then_block:Block; else_block:Optional[Block]
@dataclass
class While: cond:"Expr"; body:Block
@dataclass
class ExprStmt: value:"Expr"
Stmt=Union[Let,Assign,Return,If,While,ExprStmt]
@dataclass
class IntLit: value:int
@dataclass
class BoolLit: value:bool
@dataclass
class Var: name:str
@dataclass
class Unary: op:str; expr:"Expr"
@dataclass
class Binary: op:str; left:"Expr"; right:"Expr"
@dataclass
class Call: name:str; args:list["Expr"]
Expr=Union[IntLit,BoolLit,Var,Unary,Binary,Call]

class Parser:
    def __init__(self,tokens): self.t=tokens; self.i=0
    def cur(self): return self.t[self.i]
    def eat(self,kind):
        tok=self.cur()
        if tok.kind!=kind: raise CompileError(f"expected {kind} at byte {tok.pos}, got {tok.kind}")
        self.i+=1; return tok
    def maybe(self,kind):
        if self.cur().kind==kind: return self.eat(kind)
        return None
    def parse_program(self):
        fs=[]
        while self.cur().kind!="EOF": fs.append(self.parse_function())
        if not fs: raise CompileError("program must define at least one function")
        return Program(fs)
    def parse_function(self):
        self.eat("FN"); name=self.eat("IDENT").text; self.eat("("); params=[]
        if self.cur().kind!=")":
            while True:
                pn=self.eat("IDENT").text; self.eat(":"); pt=self.parse_type(); params.append(Param(pn,pt))
                if not self.maybe(","): break
        self.eat(")"); self.eat("->"); rt=self.parse_type(); return Function(name,params,rt,self.parse_block())
    def parse_type(self):
        if self.cur().kind in ("INT","BOOL"): return self.eat(self.cur().kind).text
        raise CompileError(f"expected type at byte {self.cur().pos}")
    def parse_block(self):
        self.eat("{"); ss=[]
        while self.cur().kind!="}":
            if self.cur().kind=="EOF": raise CompileError("unterminated block")
            ss.append(self.parse_stmt())
        self.eat("}"); return Block(ss)
    def parse_stmt(self):
        k=self.cur().kind
        if k=="LET":
            self.eat("LET"); n=self.eat("IDENT").text; self.eat(":"); typ=self.parse_type(); self.eat("="); e=self.parse_expr(); self.eat(";"); return Let(n,typ,e)
        if k=="RETURN":
            self.eat("RETURN"); e=self.parse_expr(); self.eat(";"); return Return(e)
        if k=="IF":
            self.eat("IF"); self.eat("("); c=self.parse_expr(); self.eat(")"); tb=self.parse_block(); eb=None
            if self.maybe("ELSE"): eb=self.parse_block()
            return If(c,tb,eb)
        if k=="WHILE":
            self.eat("WHILE"); self.eat("("); c=self.parse_expr(); self.eat(")"); return While(c,self.parse_block())
        if k=="IDENT" and self.t[self.i+1].kind=="=":
            n=self.eat("IDENT").text; self.eat("="); e=self.parse_expr(); self.eat(";"); return Assign(n,e)
        e=self.parse_expr(); self.eat(";"); return ExprStmt(e)
    def parse_expr(self): return self.parse_or()
    def parse_or(self):
        e=self.parse_and()
        while self.maybe("||"): e=Binary("||",e,self.parse_and())
        return e
    def parse_and(self):
        e=self.parse_eq()
        while self.maybe("&&"): e=Binary("&&",e,self.parse_eq())
        return e
    def parse_eq(self):
        e=self.parse_rel()
        while self.cur().kind in ("==","!="):
            op=self.eat(self.cur().kind).text; e=Binary(op,e,self.parse_rel())
        return e
    def parse_rel(self):
        e=self.parse_add()
        while self.cur().kind in ("<","<=",">",">="):
            op=self.eat(self.cur().kind).text; e=Binary(op,e,self.parse_add())
        return e
    def parse_add(self):
        e=self.parse_mul()
        while self.cur().kind in ("+","-"):
            op=self.eat(self.cur().kind).text; e=Binary(op,e,self.parse_mul())
        return e
    def parse_mul(self):
        e=self.parse_unary()
        while self.cur().kind in ("*","/","%"):
            op=self.eat(self.cur().kind).text; e=Binary(op,e,self.parse_unary())
        return e
    def parse_unary(self):
        if self.cur().kind in ("!","-"):
            op=self.eat(self.cur().kind).text; return Unary(op,self.parse_unary())
        return self.parse_primary()
    def parse_primary(self):
        tok=self.cur()
        if tok.kind=="INT": self.i+=1; return IntLit(int(tok.text))
        if tok.kind=="TRUE": self.i+=1; return BoolLit(True)
        if tok.kind=="FALSE": self.i+=1; return BoolLit(False)
        if tok.kind=="IDENT":
            self.i+=1; name=tok.text
            if self.maybe("("):
                args=[]
                if self.cur().kind!=")":
                    while True:
                        args.append(self.parse_expr())
                        if not self.maybe(","): break
                self.eat(")"); return Call(name,args)
            return Var(name)
        if self.maybe("("):
            e=self.parse_expr(); self.eat(")"); return e
        raise CompileError(f"expected expression at byte {tok.pos}")

def block_returns(b:Block)->bool:
    for s in b.statements:
        if isinstance(s,Return): return True
        if isinstance(s,If) and s.else_block and block_returns(s.then_block) and block_returns(s.else_block): return True
    return False

class Checker:
    def __init__(self,p): self.p=p; self.sigs={}
    def check(self):
        for f in self.p.functions:
            if f.name in self.sigs: raise CompileError(f"duplicate function {f.name}")
            seen=set()
            for p in f.params:
                if p.name in seen: raise CompileError(f"duplicate parameter {p.name} in {f.name}")
                seen.add(p.name)
            self.sigs[f.name]=([p.type_name for p in f.params],f.ret_type)
        if "main" not in self.sigs: raise CompileError("program must define main")
        for f in self.p.functions: self.check_function(f)
    def check_function(self,f):
        env={p.name:p.type_name for p in f.params}; self.check_block(f.body,env,f.ret_type)
        if not block_returns(f.body): raise CompileError(f"function {f.name} does not return on all obvious paths")
    def check_block(self,b,env,ret):
        local=dict(env)
        for s in b.statements:
            if isinstance(s,Let):
                if s.name in local: raise CompileError(f"duplicate/shadowed variable {s.name}")
                t=self.type_expr(s.value,local)
                if t!=s.type_name: raise CompileError(f"let {s.name}: expected {s.type_name}, got {t}")
                local[s.name]=s.type_name
            elif isinstance(s,Assign):
                if s.name not in local: raise CompileError(f"assignment to unknown variable {s.name}")
                t=self.type_expr(s.value,local)
                if t!=local[s.name]: raise CompileError(f"assignment {s.name}: expected {local[s.name]}, got {t}")
            elif isinstance(s,Return):
                t=self.type_expr(s.value,local)
                if t!=ret: raise CompileError(f"return expected {ret}, got {t}")
            elif isinstance(s,If):
                if self.type_expr(s.cond,local)!="bool": raise CompileError("if condition must be bool")
                self.check_block(s.then_block,local,ret)
                if s.else_block: self.check_block(s.else_block,local,ret)
            elif isinstance(s,While):
                if self.type_expr(s.cond,local)!="bool": raise CompileError("while condition must be bool")
                self.check_block(s.body,local,ret)
            elif isinstance(s,ExprStmt): self.type_expr(s.value,local)
    def type_expr(self,e,env):
        if isinstance(e,IntLit): return "int"
        if isinstance(e,BoolLit): return "bool"
        if isinstance(e,Var):
            if e.name not in env: raise CompileError(f"unknown variable {e.name}")
            return env[e.name]
        if isinstance(e,Unary):
            t=self.type_expr(e.expr,env)
            if e.op=="-" and t=="int": return "int"
            if e.op=="!" and t=="bool": return "bool"
            raise CompileError(f"bad unary {e.op} for {t}")
        if isinstance(e,Binary):
            a=self.type_expr(e.left,env); b=self.type_expr(e.right,env)
            if e.op in ("+","-","*","/","%") and a==b=="int": return "int"
            if e.op in ("<","<=",">",">=") and a==b=="int": return "bool"
            if e.op in ("==","!=") and a==b: return "bool"
            if e.op in ("&&","||") and a==b=="bool": return "bool"
            raise CompileError(f"bad binary {e.op} for {a},{b}")
        if isinstance(e,Call):
            if e.name not in self.sigs: raise CompileError(f"unknown function {e.name}")
            ps,rt=self.sigs[e.name]
            if len(ps)!=len(e.args): raise CompileError(f"{e.name} expects {len(ps)} args, got {len(e.args)}")
            for i,(want,arg) in enumerate(zip(ps,e.args),1):
                got=self.type_expr(arg,env)
                if got!=want: raise CompileError(f"{e.name} arg {i}: expected {want}, got {got}")
            return rt
        raise AssertionError(type(e))

def parse_source(src:str)->Program:
    p=Parser(lex(src)).parse_program(); Checker(p).check(); return p

def ast_json(p): return json.dumps(asdict(p),indent=2)

def main(argv=None):
    argv=sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage: elite_frontend.py [--tokens|--ast|--check] FILE",file=sys.stderr); return 2
    mode="--check"
    if argv[0].startswith("--"): mode=argv.pop(0)
    if len(argv)!=1: print("expected one source file",file=sys.stderr); return 2
    try:
        src=open(argv[0],encoding="utf-8").read()
        if mode=="--tokens":
            for t in lex(src): print(f"{t.kind:10} {t.text!r} @{t.pos}")
            return 0
        p=parse_source(src)
        if mode=="--ast": print(ast_json(p))
        elif mode=="--check": print("OK")
        else: raise CompileError(f"unknown mode {mode}")
        return 0
    except (OSError,CompileError) as e:
        print(f"error: {e}",file=sys.stderr); return 1

if __name__=="__main__": raise SystemExit(main())

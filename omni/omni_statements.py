"""Statement AST for assignments, returns, calls and conditionals."""
from __future__ import annotations
from dataclasses import dataclass
from .omni_expr import Expr

class Stmt: pass
@dataclass(frozen=True)
class Assign(Stmt):
    name: str
    value: Expr
@dataclass(frozen=True)
class Return(Stmt):
    value: Expr|None = None
@dataclass(frozen=True)
class Call(Stmt):
    function: str
    arguments: tuple[Expr,...] = ()
    result: str|None = None
@dataclass(frozen=True)
class If(Stmt):
    condition: Expr
    then_body: tuple[Stmt,...]
    else_body: tuple[Stmt,...] = ()

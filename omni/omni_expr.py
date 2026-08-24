"""Small executable expression model for the Omni source pipeline."""
from __future__ import annotations
from dataclasses import dataclass

class Expr: pass
@dataclass(frozen=True)
class IntLiteral(Expr): value:int
@dataclass(frozen=True)
class Variable(Expr): name:str
@dataclass(frozen=True)
class Binary(Expr): op:str; left:Expr; right:Expr

def evaluate(expr, env=None):
    env={} if env is None else env
    if isinstance(expr,IntLiteral): return expr.value
    if isinstance(expr,Variable): return env[expr.name]
    if isinstance(expr,Binary):
        a,b=evaluate(expr.left,env),evaluate(expr.right,env)
        if expr.op=='+': return a+b
        if expr.op=='-': return a-b
        if expr.op=='*': return a*b
        if expr.op=='/': return a//b
        raise ValueError(f'unknown binary operator: {expr.op}')
    raise TypeError(f'unknown expression: {type(expr).__name__}')

"""Structured loop statement for Omni control-flow lowering."""
from __future__ import annotations
from dataclasses import dataclass
from .omni_expr import Expr
from .omni_statements import Stmt

@dataclass(frozen=True)
class While(Stmt):
    condition: Expr
    body: tuple[Stmt,...]

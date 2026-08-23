"""Lower simple compare/branch operations to x86-64 bytes."""
from __future__ import annotations
from dataclasses import dataclass
from .native_machine_ops import cmp_rr, je_rel8, jne_rel8, jmp_rel8

@dataclass(frozen=True)
class BranchPlan:
    condition: str
    left: int
    right: int
    true_delta: int
    false_delta: int | None = None

def lower_branch(condition:str,left:int,right:int,true_delta:int,false_delta=None)->BranchPlan:
    if condition not in {"eq","ne"}:
        raise ValueError("only eq/ne are currently supported")
    return BranchPlan(condition,left,right,true_delta,false_delta)

def encode_branch(plan:BranchPlan)->bytes:
    code=cmp_rr(plan.left,plan.right)
    if plan.condition=="eq":
        code += je_rel8(plan.true_delta)
    else:
        code += jne_rel8(plan.true_delta)
    if plan.false_delta is not None:
        code += jmp_rel8(plan.false_delta)
    return code

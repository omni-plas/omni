"""Lower simple compare/branch operations to x86-64 bytes."""
from __future__ import annotations
from dataclasses import dataclass
from .native_machine_ops import cmp_rr, je_rel8, jne_rel8, jmp_rel8
from .native_relocations import Relocation

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
    code += je_rel8(plan.true_delta) if plan.condition=="eq" else jne_rel8(plan.true_delta)
    if plan.false_delta is not None: code += jmp_rel8(plan.false_delta)
    return code

def encode_labeled_branch(condition:str,left:int,right:int,true_target:int,false_target:int|None=None):
    code=bytearray(cmp_rr(left,right))
    code += b"\x74\x00" if condition=="eq" else b"\x75\x00"
    relocs=[Relocation(len(code)-1,true_target,1)]
    if false_target is not None:
        code += b"\xeb\x00"
        relocs.append(Relocation(len(code)-1,false_target,1))
    return bytes(code),tuple(relocs)

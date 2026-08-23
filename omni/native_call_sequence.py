"""Plan call sequences around native function frames."""
from __future__ import annotations
from dataclasses import dataclass
from .native_call_lowering import lower_call, move_arguments

@dataclass(frozen=True)
class CallSequence:
    target: str
    moves: bytes
    stack_argument_count: int

def build_call_sequence(target:str,args:tuple[int,...])->CallSequence:
    plan=lower_call(target,args)
    return CallSequence(target,move_arguments(plan),len(plan.stack_arguments))

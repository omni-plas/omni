"""Lower integer calls using the x86-64 System V ABI."""
from __future__ import annotations
from dataclasses import dataclass
from .native_abi import ARG_REGISTERS
from .native_machine_ops import mov_rr

@dataclass(frozen=True)
class CallPlan:
    target: str
    argument_registers: tuple[int,...]
    stack_arguments: tuple[int,...]

def lower_call(target:str, args:tuple[int,...])->CallPlan:
    register_args=tuple(args[:len(ARG_REGISTERS)])
    stack_args=tuple(args[len(ARG_REGISTERS):])
    return CallPlan(target,register_args,stack_args)

def move_arguments(plan:CallPlan)->bytes:
    if plan.stack_arguments:
        raise NotImplementedError("stack argument stores require call-frame lowering")
    out=bytearray()
    for src,dst in zip(plan.argument_registers,ARG_REGISTERS):
        if src != dst: out += mov_rr(dst,src)
    return bytes(out)

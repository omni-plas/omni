"""Concrete integer call lowering using the x86-64 System V ABI."""
from __future__ import annotations
from dataclasses import dataclass
from .native_abi import ARG_REGISTERS
from .native_calling_convention import RETURN_REGISTER
from .native_machine_ops import mov_rr, call_rel32

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

def emit_call(rel32:int)->bytes:
    return call_rel32(rel32)

def move_call_arguments(values, register_map):
    out=bytearray()
    if len(values)>len(ARG_REGISTERS):
        raise ValueError('stack arguments require stack-frame lowering')
    for index,value in enumerate(values):
        src=register_map[value]; dst=ARG_REGISTERS[index]
        if src != dst: out += mov_rr(dst,src)
    return bytes(out)

def emit_direct_call(rel32:int):
    return call_rel32(rel32)

def move_return_value(source_register:int):
    if source_register==RETURN_REGISTER:
        return b''
    return mov_rr(RETURN_REGISTER,source_register)

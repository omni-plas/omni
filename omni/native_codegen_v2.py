"""Spill-aware adapter for native functions.

This keeps the bootstrap emitter intact while providing a concrete lowering
entry point that consumes the shared allocation/frame model.
"""
from __future__ import annotations
from dataclasses import dataclass
from .native_allocating_emitter import prepare_native_function
from .native_machine_ops import mov_rr, mov_imm64, add_rr, sub_rr, imul_rr

@dataclass(frozen=True)
class NativeInstruction:
    opcode: str
    operands: tuple[int, ...]

@dataclass(frozen=True)
class PreparedCode:
    name: str
    stack_size: int
    instructions: tuple[NativeInstruction, ...]

def prepare(fn, registers=(3,4,5,10,11,12,13,14,15)) -> PreparedCode:
    allocation = prepare_native_function(fn, registers)
    instructions=[]
    for value in allocation.allocation.values:
        if value.location.register is not None:
            instructions.append(NativeInstruction("reg", (value.location.register,)))
        else:
            instructions.append(NativeInstruction("spill", (value.location.stack_offset,)))
    return PreparedCode(fn.name, allocation.frame.stack_size, tuple(instructions))

def encode_instruction(instruction: NativeInstruction) -> bytes:
    if instruction.opcode == "mov" and len(instruction.operands)==2: return mov_rr(*instruction.operands)
    if instruction.opcode == "imm" and len(instruction.operands)==2: return mov_imm64(*instruction.operands)
    if instruction.opcode == "add" and len(instruction.operands)==2: return add_rr(*instruction.operands)
    if instruction.opcode == "sub" and len(instruction.operands)==2: return sub_rr(*instruction.operands)
    if instruction.opcode == "imul" and len(instruction.operands)==2: return imul_rr(*instruction.operands)
    raise ValueError(f"unsupported native instruction: {instruction.opcode}")

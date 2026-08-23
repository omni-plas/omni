"""Small lowering layer between Omni IR and target machine emission."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ValueLocation:
    register: int | None = None
    stack_offset: int | None = None

@dataclass(frozen=True)
class LoweredInstruction:
    opcode: str
    operands: tuple[object, ...] = ()

@dataclass(frozen=True)
class LoweredFunction:
    name: str
    instructions: tuple[LoweredInstruction, ...]
    stack_size: int = 0

def lower_return(register: int) -> LoweredInstruction:
    return LoweredInstruction("return_reg", (register,))

def lower_move(src: ValueLocation, dst: ValueLocation) -> tuple[LoweredInstruction, ...]:
    if dst.register is not None and src.register is not None:
        return (LoweredInstruction("mov_rr", (dst.register, src.register)),)
    if dst.register is not None and src.stack_offset is not None:
        return (LoweredInstruction("reload", (dst.register, src.stack_offset)),)
    if dst.stack_offset is not None and src.register is not None:
        return (LoweredInstruction("spill", (dst.stack_offset, src.register)),)
    raise ValueError("memory-to-memory move requires a scratch register")

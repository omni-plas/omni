"""Compute stable RBP-relative locations for native spill slots."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class FrameSlot:
    value: str
    rbp_offset: int

@dataclass(frozen=True)
class FunctionFrame:
    stack_size: int
    slots: tuple[FrameSlot, ...]

def build_function_frame(spills: dict[str,int], stack_size: int) -> FunctionFrame:
    if stack_size < 0 or stack_size % 16:
        raise ValueError("native frame must be 16-byte aligned")
    slots = tuple(FrameSlot(name, -(offset + 8)) for name, offset in sorted(spills.items()))
    if slots and max(abs(s.rbp_offset) for s in slots) > stack_size:
        raise ValueError("spill slot exceeds frame")
    return FunctionFrame(stack_size, slots)

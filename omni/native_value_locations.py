"""Resolve allocator output into register or frame-backed locations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_allocator_codegen import allocate_function
from .native_function_frame import build_function_frame

@dataclass(frozen=True)
class ResolvedValue:
    name: str
    register: int | None
    rbp_offset: int | None

def resolve_function(fn, registers=(3,4,5,10,11,12,13,14,15)) -> tuple[ResolvedValue,...]:
    allocation=allocate_function(fn, registers)
    spills={v.name:v.location.stack_offset for v in allocation.values if v.location.stack_offset is not None}
    frame=build_function_frame(spills, allocation.stack_size)
    frame_offsets={s.value:s.rbp_offset for s in frame.slots}
    return tuple(ResolvedValue(v.name, v.location.register, frame_offsets.get(v.name)) for v in allocation.values)

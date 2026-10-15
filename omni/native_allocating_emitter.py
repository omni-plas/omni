"""Allocator-backed native emission facade.

The existing bootstrap emitter remains the compatibility implementation;
this facade makes the shared allocation plan an explicit prerequisite for
native emission and exposes the locations required by a future full lowering.
"""
from __future__ import annotations
from dataclasses import dataclass
from .native_allocator_codegen import allocate_function
from .native_function_frame import build_function_frame

@dataclass(frozen=True)
class PreparedNativeFunction:
    allocation: object
    frame: object

    @property
    def values(self):
        """Expose allocated value locations without leaking allocator internals."""
        return self.allocation.values

def prepare_native_function(fn, registers=(3,4,5,10,11,12,13,14,15)) -> PreparedNativeFunction:
    allocation = allocate_function(fn, registers)
    spills = {v.name: v.location.stack_offset for v in allocation.values if v.location.stack_offset is not None}
    frame = build_function_frame(spills, allocation.stack_size)
    return PreparedNativeFunction(allocation, frame)

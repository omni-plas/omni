"""Compile the supported FunctionIR subset directly to ELF64 bytes."""
from __future__ import annotations
from .native_ir_emitter import lower_function, emit_lowered
from .native_value_locations import resolve_function

def compile_function_to_elf(fn, registers=(3,4,5,10,11,12,13,14,15)) -> bytes:
    resolved = resolve_function(fn, registers)
    locations = {v.name: v.register for v in resolved if v.register is not None}
    if len(locations) != len(resolved):
        raise NotImplementedError("spilled IR values require spill-aware IR lowering")
    lowered = lower_function(fn, locations)
    return emit_lowered(lowered).code

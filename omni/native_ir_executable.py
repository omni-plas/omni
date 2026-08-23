"""Compile the supported FunctionIR subset directly to native bytes."""
from __future__ import annotations
from .native_ir_emitter import lower_function, emit_lowered
from .native_value_locations import resolve_function
from .native_spill_ir import materialize_locations, reload

def compile_function_to_native(fn, registers=(3,4,5,10,11,12,13,14,15)) -> bytes:
    resolved = resolve_function(fn, registers)
    materialized = materialize_locations(resolved)
    locations = {v.name: v.register for v in materialized}
    # Reloads are represented at the materialization boundary; the existing
    # lowering then operates on the selected physical registers.
    _ = tuple(reload(v) for v in materialized)
    lowered = lower_function(fn, locations)
    return emit_lowered(lowered).code


def compile_function_to_elf(fn, registers=(3,4,5,10,11,12,13,14,15)) -> bytes:
    from .elf64 import build_elf64
    return build_elf64(compile_function_to_native(fn, registers))

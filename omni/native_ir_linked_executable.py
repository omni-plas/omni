"""Compile multiple FunctionIR functions and resolve internal calls."""
from __future__ import annotations
from .native_ir_executable import compile_function_to_native
from .native_ir_emitter import lower_function, emit_lowered
from .native_value_locations import resolve_function
from .native_spill_ir import materialize_locations, reload
from .native_call_linker import link_functions

def compile_functions_to_native(functions, registers=(3,4,5,10,11,12,13,14,15)):
    emitted=[]
    for fn in functions:
        resolved=resolve_function(fn,registers)
        materialized=materialize_locations(resolved)
        locations={v.name:v.register for v in materialized}
        _=tuple(reload(v) for v in materialized)
        lowered=lower_function(fn,locations)
        result=emit_lowered(lowered)
        emitted.append((result.name,result.code,result.call_sites))
    return link_functions(tuple(emitted))

def compile_functions_to_elf(functions, entry='main', registers=(3,4,5,10,11,12,13,14,15)):
    from .elf64 import build_elf64
    linked=compile_functions_to_native(functions,registers)
    if entry not in linked.symbols: raise KeyError(f'unresolved entry symbol: {entry}')
    return build_elf64(linked.code,linked.symbols[entry])

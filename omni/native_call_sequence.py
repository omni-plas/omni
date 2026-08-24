"""Build a concrete internal-call byte sequence around ABI lowering."""
from __future__ import annotations
from .native_call_lowering import move_call_arguments, emit_direct_call, move_return_value

def lower_internal_call(values, register_map, rel32, result_register=None):
    code=bytearray(move_call_arguments(values,register_map))
    code += emit_direct_call(rel32)
    if result_register is not None:
        code += move_return_value(result_register)
    return bytes(code)

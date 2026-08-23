"""Compile multiple FunctionIR values into one linked native module."""
from __future__ import annotations
from dataclasses import dataclass
from .native_ir_executable import compile_function_to_native
from .native_module_linker import NativeFragment, link_fragments

@dataclass(frozen=True)
class CompiledFunction:
    name: str
    code: bytes

def compile_functions(functions, registers=(3,4,5,10,11,12,13,14,15)):
    compiled=tuple(CompiledFunction(fn.name,compile_function_to_native(fn,registers)) for fn in functions)
    return link_fragments(tuple(NativeFragment(x.name,x.code) for x in compiled))

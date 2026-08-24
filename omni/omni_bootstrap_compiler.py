"""Bootstrap compiler facade: Omni source -> frontend units -> native module."""
from __future__ import annotations
from .omni_source_frontend import parse_source
from .native_function_module import CompiledFunction
from .native_module_linker import NativeFragment, link_fragments

def compile_source(source:str, compile_body):
    """Compile parsed Omni functions using a supplied body lowering function."""
    functions=parse_source(source)
    fragments=[]
    for fn in functions:
        code=bytes(compile_body(fn))
        fragments.append(NativeFragment(fn.name,code))
    return link_fragments(tuple(fragments))

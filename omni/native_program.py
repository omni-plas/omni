"""Compose functions, entrypoint and data into a native program artifact."""
from __future__ import annotations
from dataclasses import dataclass
from .native_function_module import compile_functions
from .native_executable_pipeline import link_module
from .native_module_linker import NativeFragment

@dataclass(frozen=True)
class NativeProgram:
    image: object
    functions: tuple[str,...]

def build_program(functions, entry):
    module=compile_functions(tuple(functions))
    fragment=NativeFragment('__linked__',module.code)
    image=link_module((fragment,),None)
    symbols=dict(module.symbols)
    return NativeProgram(image,tuple(symbols))

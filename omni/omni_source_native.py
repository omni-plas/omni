"""Source-to-native pipeline without an injected body-lowering callback."""
from __future__ import annotations
from .omni_compiler_pipeline import compile_source_to_ir
from .omni_ir_native_lowering import lower_module
from .native_operation_lowering import lower_operations
from .native_module_linker import NativeFragment, link_fragments

def compile_source_to_native(source: str):
    ir=compile_source_to_ir(source)
    functions=lower_module(ir)
    fragments=[]
    for fn in functions:
        code=lower_operations(fn.blocks[0].operations,{})
        fragments.append(NativeFragment(fn.name,code))
    return link_fragments(tuple(fragments))

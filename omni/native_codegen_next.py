"""Allocator-aware facade for the next native backend generation path."""
from __future__ import annotations
from .native_multi_codegen import emit_multi_x86_64_elf
from .native_backend_executor import prepare_function

def prepare_module_functions(module, registers=(3,4,5,10,11,12,13,14,15)):
    module.validate()
    return tuple(prepare_function(fn, tuple(registers)) for fn in module.functions)

def emit(module, target=None):
    # Keep the established emitter as the compatibility path while all
    # functions are prepared through the shared allocator contract first.
    prepare_module_functions(module)
    return emit_multi_x86_64_elf(module, target)

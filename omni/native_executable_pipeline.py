"""Compose linked native code into an ELF64 executable image."""
from __future__ import annotations
from .native_module_linker import link_fragments, NativeFragment
from .elf64 import build_elf64

def build_linked_executable(fragments, entry_symbol=None):
    module=link_fragments(tuple(fragments))
    entry=0 if entry_symbol is None else module.symbols[entry_symbol]
    return build_elf64(module.code, entry)

def build_single_function_executable(name, code):
    return build_linked_executable((NativeFragment(name, bytes(code)),), name)

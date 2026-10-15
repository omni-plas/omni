"""Compose linked native code into an ELF64 executable image."""
from __future__ import annotations
from dataclasses import dataclass
from .native_module_linker import link_fragments, NativeFragment
from .elf64 import build_elf64

@dataclass(frozen=True)
class ExecutableImage:
    data: bytes
    entry_offset: int
    symbols: dict[str, int]

def build_linked_executable(fragments, entry_symbol=None) -> ExecutableImage:
    """Link fragments and retain executable metadata alongside the ELF bytes."""
    return link_module(fragments, entry_symbol)

def link_module(fragments, entry_symbol=None) -> ExecutableImage:
    module=link_fragments(tuple(fragments))
    if not module.code:
        raise ValueError("cannot build empty executable")
    entry=0 if entry_symbol is None else module.symbols[entry_symbol]
    data=build_elf64(module.code, entry)
    return ExecutableImage(data, entry, dict(module.symbols))

def build_single_function_executable(name, code):
    return build_linked_executable((NativeFragment(name, bytes(code)),), name).data

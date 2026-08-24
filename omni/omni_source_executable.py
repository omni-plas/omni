"""Build an ELF image directly from the supported Omni source subset."""
from __future__ import annotations
from .omni_source_native import compile_source_to_native
from .elf64 import build_elf64

def compile_source_to_elf(source: str, entry_symbol: str = "main") -> bytes:
    module=compile_source_to_native(source)
    if entry_symbol not in module.symbols:
        raise ValueError(f"entry symbol not found: {entry_symbol}")
    return build_elf64(module.code,module.symbols[entry_symbol])

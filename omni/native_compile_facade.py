"""Validated facade over Omni's self-contained x86-64 ELF backend."""
from __future__ import annotations
from .native_codegen import emit_x86_64_elf, NativeExecutable

def compile_module(module, target=None) -> NativeExecutable:
    return emit_x86_64_elf(module, target)

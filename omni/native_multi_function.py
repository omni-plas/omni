"""Assemble several named native functions into one linked module."""
from __future__ import annotations
from dataclasses import dataclass
from .native_module_linker import NativeFragment, link_fragments

@dataclass(frozen=True)
class FunctionFragment:
    name:str
    code:bytes

def build_function_module(functions):
    fragments=tuple(NativeFragment(f.name,bytes(f.code)) for f in functions)
    return link_fragments(fragments)

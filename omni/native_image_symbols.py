"""Resolve code/data symbols against one native image address space."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SymbolAddress:
    name: str
    offset: int
    section: str

def resolve_symbols(code_symbols, data_symbols, code_size):
    result={}
    for name, offset in code_symbols.items():
        if name in result: raise ValueError(f"duplicate symbol: {name}")
        result[name]=SymbolAddress(name,offset,"code")
    for name, offset in data_symbols.items():
        if name in result: raise ValueError(f"duplicate symbol: {name}")
        result[name]=SymbolAddress(name,code_size+offset,"data")
    return result

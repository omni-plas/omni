"""Validated symbol table for internal native functions."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
    name:str
    offset:int
    size:int

def build_symbol_table(functions):
    table={}; cursor=0
    for fn in functions:
        if fn.name in table: raise ValueError(f'duplicate symbol: {fn.name}')
        table[fn.name]=Symbol(fn.name,cursor,len(fn.code)); cursor += len(fn.code)
    return table

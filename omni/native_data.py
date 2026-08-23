"""Deterministic read-only/data layout for native modules."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DataSymbol:
    name:str
    offset:int
    data:bytes

@dataclass(frozen=True)
class DataSection:
    data:bytes
    symbols:dict[str,int]

def layout_data(items):
    cursor=0; chunks=[]; symbols={}
    for name,data in items:
        if name in symbols: raise ValueError(f"duplicate data symbol: {name}")
        raw=bytes(data); symbols[name]=cursor; chunks.append(raw); cursor+=len(raw)
    return DataSection(b"".join(chunks),symbols)

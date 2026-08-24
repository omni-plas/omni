"""Deterministic module/function placement for native images."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class FunctionPlacement:
    name:str
    offset:int
    size:int

def layout_functions(functions):
    offset=0; placements=[]
    for name,code in functions:
        blob=bytes(code)
        placements.append(FunctionPlacement(name,offset,len(blob)))
        offset += len(blob)
    return tuple(placements),offset

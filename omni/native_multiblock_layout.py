"""Deterministic layout model for native basic blocks."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BlockPlacement:
    name:str
    offset:int
    size:int

def layout_blocks(blocks):
    offset=0; result=[]
    for name,code in blocks:
        blob=bytes(code)
        result.append(BlockPlacement(name,offset,len(blob)))
        offset += len(blob)
    return tuple(result),offset

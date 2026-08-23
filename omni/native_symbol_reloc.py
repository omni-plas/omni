"""Typed symbol relocations shared by native linker stages."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SymbolRelocation:
    kind: str
    immediate_offset: int
    symbol: str
    addend: int = 0
    instruction_end: int | None = None

def call_rel32(offset:int,symbol:str,instruction_end:int,addend:int=0):
    return SymbolRelocation("call_rel32",offset,symbol,addend,instruction_end)

def abs32(offset:int,symbol:str,addend:int=0):
    return SymbolRelocation("abs32",offset,symbol,addend,None)

def abs64(offset:int,symbol:str,addend:int=0):
    return SymbolRelocation("abs64",offset,symbol,addend,None)
